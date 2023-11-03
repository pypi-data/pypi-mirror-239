import numpy as np
from attrs import define, field, validators
from datetime import timedelta, time
from time import sleep
from itertools import product
from volstreet.config import logger
from volstreet.blackscholes import Greeks
from volstreet.utils.core import (
    time_to_expiry,
    current_time,
    find_strike,
    find_strike_with_offset,
    extend_strike_range,
)
from volstreet.utils.communication import notifier
from volstreet.utils.data_io import load_json_data, load_combine_save_json_data
from volstreet.dealingroom import (
    Index,
    Strangle,
    Straddle,
    Option,
    place_option_order_and_notify,
)
from volstreet.angel_interface.active_session import ActiveSession


@define(slots=False)
class DeltaPositionMonitor:
    underlying: Index = field(validator=validators.instance_of(Index))
    instrument: Straddle | Strangle = field(
        validator=validators.instance_of((Straddle, Strangle, Option))
    )
    initial_position_info: dict = field(validator=validators.instance_of(dict))
    _call_active_qty = field()
    _put_active_qty = field()
    _total_premium = field()
    underlying_ltp: float = field(
        validator=validators.instance_of((int, float)), repr=False, default=np.nan
    )
    call_ltp: float = field(
        validator=validators.instance_of((int, float)), repr=False, default=np.nan
    )
    put_ltp: float = field(
        validator=validators.instance_of((int, float)), repr=False, default=np.nan
    )
    call_greeks: Greeks = field(init=False, repr=False, factory=Greeks)
    put_greeks: Greeks = field(init=False, repr=False, factory=Greeks)
    position_greeks: Greeks = field(init=False, repr=False, factory=Greeks)
    exit_triggers: dict[str, bool] = field(
        factory=lambda: {"end_time": False, "qty_breach_exit": False}
    )
    notifier_url: str = field(default=None, repr=False)

    @_call_active_qty.default
    def _call_active_qty_default(self):
        return self.initial_position_info["Initial Qty"] * -1

    @_put_active_qty.default
    def _put_active_qty_default(self):
        return self.initial_position_info["Initial Qty"] * -1

    @_total_premium.default
    def _total_premium_default(self):
        return (
            self.initial_position_info["Initial Qty"]
            * self.initial_position_info["Total Entry Price"]
        )

    @property
    def call_active_qty(self):
        return self._call_active_qty

    @call_active_qty.setter
    def call_active_qty(self, value):
        self._call_active_qty = int(value)
        self.update_position_greeks()

    @property
    def put_active_qty(self):
        return self._put_active_qty

    @put_active_qty.setter
    def put_active_qty(self, value):
        self._put_active_qty = int(value)
        self.update_position_greeks()

    @property
    def total_premium(self):
        return self._total_premium

    @total_premium.setter
    def total_premium(self, value):
        self._total_premium = float(value)

    @property
    def mark_to_market(self) -> float | int:
        return (self.call_active_qty * self.call_ltp) + (
            self.put_active_qty * self.put_ltp
        )

    @property
    def pnl(self) -> float | int:
        return self.total_premium + self.mark_to_market

    def update_prices_and_greeks(self) -> None:
        # Fetching prices
        underlying_ltp = self.underlying.fetch_ltp()
        call_ltp, put_ltp = self.instrument.fetch_ltp()
        tte = time_to_expiry(self.instrument.expiry)
        call_greeks, put_greeks = self.instrument.fetch_greeks(
            spot=underlying_ltp,
            prices=(call_ltp, put_ltp),
            t=tte,
        )
        self.underlying_ltp = underlying_ltp
        self.call_ltp = call_ltp
        self.put_ltp = put_ltp
        self.call_greeks = call_greeks
        self.put_greeks = put_greeks
        self.update_position_greeks()

    def _update_active_qty_and_premium(
        self,
        is_call: bool,
        adjustment_qty: int | float,
        avg_price: float,
    ) -> None:
        """If adjustment qty is positive, it means that the position is being squared up."""
        active_qty = self.call_active_qty if is_call else self.put_active_qty
        active_qty = active_qty + adjustment_qty

        self.total_premium = self.total_premium - (adjustment_qty * avg_price)

        if is_call:
            self.call_active_qty = active_qty
        else:
            self.put_active_qty = active_qty

    def update_call_active_qty_and_premium(
        self,
        adjustment_qty: int,
        avg_price: float,
    ) -> None:
        self._update_active_qty_and_premium(True, adjustment_qty, avg_price)

    def update_put_active_qty_and_premium(
        self,
        adjustment_qty: int,
        avg_price: float,
    ) -> None:
        self._update_active_qty_and_premium(False, adjustment_qty, avg_price)

    def update_position_greeks(self) -> None:
        call_position_greeks: Greeks = self.call_greeks * self.call_active_qty
        put_position_greeks: Greeks = self.put_greeks * self.put_active_qty
        position_greeks: Greeks = call_position_greeks + put_position_greeks
        self.position_greeks = position_greeks

    def recommend_delta_action(
        self,
        straddle: Straddle,
        delta_threshold: float,
    ) -> tuple[Straddle, int] | tuple[None, np.nan]:
        position_delta = self.position_greeks.delta

        if (
            position_delta >= delta_threshold
        ):  # Net delta is positive, sell the required qty of calls
            qty_to_sell = int((abs(position_delta) - 0) / abs(self.call_greeks.delta))
            instrument_to_sell = straddle.call_option
        elif (
            position_delta <= -delta_threshold
        ):  # Net delta is negative, sell the required qty of puts
            qty_to_sell = int((abs(position_delta) - 0) / abs(self.put_greeks.delta))
            instrument_to_sell = straddle.put_option
        else:
            return None, np.nan

        return (None, np.nan) if qty_to_sell == 0 else (instrument_to_sell, qty_to_sell)

    def check_for_breach(
        self,
        instrument: Option,
        adjustment_qty: int,
        max_qty_shares: int,
    ) -> bool:
        if instrument.option_type.lower().startswith("c"):
            breach = (abs(self.call_active_qty) + adjustment_qty) > max_qty_shares
        elif instrument.option_type.lower().startswith("p"):
            breach = (abs(self.put_active_qty) + adjustment_qty) > max_qty_shares
        else:
            raise ValueError("Invalid option type")
        return breach

    def process_breach(
        self,
        max_multiple: float,
    ) -> bool:
        """Check if the next eligible  strangle is the same as the current one,
        and if the evenness of deltas is within the threshold. If yes, then it should adjust the position.
        If no, then set exit_triggers["qty_breach_exit"] to True"""
        target_straddle, minimum_unevenness = most_even_strangle(
            self.underlying,
        )
        if (target_straddle == self.instrument) and (
            minimum_unevenness < (max_multiple * 0.8)
        ):  # The existing straddle is the most even one so trim the position
            new_call_qty, new_put_qty = self.determine_ideal_quantities(
                self.call_greeks.delta,
                self.put_greeks.delta,
            )
            call_adj_qty = min(abs(self.call_active_qty) - new_call_qty, 0)
            put_adj_qty = min(abs(self.put_active_qty) - new_put_qty, 0)
            self.square_up_position((call_adj_qty, put_adj_qty))
            return True
        else:  # The existing straddle is not the most even one so exit the position
            return False

    def determine_ideal_quantities(
        self,
        call_delta: float,
        put_delta: float,
    ) -> tuple[int, int]:
        """This function should return the ideal quantities of calls and puts that
        result in a delta neutral position. The quantities returned is rounded
        to the nearest lot size."""
        initial_qty = self.initial_position_info["Initial Qty"]
        if call_delta > put_delta:
            ratio = abs(call_delta) / abs(put_delta)
            call_qty, put_qty = initial_qty, initial_qty * ratio
        else:
            ratio = abs(put_delta) / abs(call_delta)
            call_qty, put_qty = initial_qty * ratio, initial_qty

        call_qty = round_shares_to_lot_size(call_qty, self.instrument.lot_size)
        put_qty = round_shares_to_lot_size(put_qty, self.instrument.lot_size)
        return call_qty, put_qty

    def update_single_side(
        self,
        option: Option,
        adjustment_qty: int,
        avg_price: float,
    ):
        if option.option_type.lower().startswith("c"):
            self.update_call_active_qty_and_premium(adjustment_qty, avg_price)
        elif option.option_type.lower().startswith("p"):
            self.update_put_active_qty_and_premium(adjustment_qty, avg_price)
        else:
            raise ValueError("Invalid option type")

    def neutralize_delta(
        self,
        instrument_to_sell: Option,
        adj_qty_lots: int,
    ) -> None:
        """
        IMPORTANT: This function neutralizes delta by SELLING the required qty of calls or puts.
        This function should update the position since it places an order
        """

        avg_price = place_option_order_and_notify(
            instrument_to_sell,
            "SELL",
            adj_qty_lots,
            "LIMIT",
            "Delta hedged straddle",
            self.notifier_url,
        )

        qty_in_shares = adj_qty_lots * instrument_to_sell.lot_size

        self.update_single_side(
            instrument_to_sell, -1 * qty_in_shares, avg_price
        )  # Negative qty since we are selling

        logger.info(
            f"Delta neutralized by selling {adj_qty_lots} lots of {instrument_to_sell}"
        )

    def square_up_position(
        self,
        quantities: tuple[int, int] = None,
    ) -> None:
        """Squares up the entire position if quantities are not provided.
        This function should also update the position since it places an order"""
        if quantities is None:
            call_square_up_qty = abs(self.call_active_qty)
            put_square_up_qty = abs(self.put_active_qty)
        else:
            call_square_up_qty, put_square_up_qty = quantities
        max_combined_qty = min(call_square_up_qty, put_square_up_qty)
        if max_combined_qty > 0:
            qty_in_lots = int(max_combined_qty / self.instrument.call_option.lot_size)
            call_avg, put_avg = place_option_order_and_notify(
                self.instrument,
                "BUY",
                qty_in_lots,
                "LIMIT",
                "Delta hedged straddle",
                self.notifier_url,
            )
            self.update_call_active_qty_and_premium(max_combined_qty, call_avg)
            self.update_put_active_qty_and_premium(max_combined_qty, put_avg)

        option_to_exit = (
            self.instrument.call_option
            if call_square_up_qty > put_square_up_qty
            else self.instrument.put_option
        )
        exit_qty = max(call_square_up_qty, put_square_up_qty) - max_combined_qty
        exit_qty_lots = int(exit_qty / option_to_exit.lot_size)
        if exit_qty > 0:
            avg = place_option_order_and_notify(
                option_to_exit,
                "BUY",
                exit_qty_lots,
                "LIMIT",
                "Delta hedged straddle",
                self.notifier_url,
            )
            self.update_single_side(option_to_exit, exit_qty, avg)

    def record_position_status(self):
        """Designed to periodically save the position status to a file."""
        date = current_time().strftime("%Y-%m-%d")
        file_path = f"{ActiveSession.obj.userId}\\{self.instrument.underlying}_delta_data\\{date}.json"

        position_status = {
            "time": current_time().strftime("%Y-%m-%d %H:%M:%S"),
            "underlying_ltp": self.underlying_ltp,
            "call_strike": self.instrument.strike,
            "put_strike": self.instrument.strike,
            "call_ltp": self.call_ltp,
            "put_ltp": self.put_ltp,
            "call_iv": self.call_greeks.iv,
            "put_iv": self.put_greeks.iv,
            "call_delta": self.call_greeks.delta,
            "put_delta": self.put_greeks.delta,
            "position_delta": self.position_greeks.delta,
            "call_theta": self.call_greeks.theta,
            "put_theta": self.put_greeks.theta,
            "position_theta": self.position_greeks.theta,
            "call_vega": self.call_greeks.vega,
            "put_vega": self.put_greeks.vega,
            "position_vega": self.position_greeks.vega,
            "call_gamma": self.call_greeks.gamma,
            "put_gamma": self.put_greeks.gamma,
            "position_gamma": self.position_greeks.gamma,
            "call_active_qty": self.call_active_qty,
            "put_active_qty": self.put_active_qty,
            "total_premium": self.total_premium,
            "mark_to_market": self.mark_to_market,
            "pnl": self.pnl,
        }
        load_combine_save_json_data(
            position_status,
            file_path,
        )


def efficient_ltp_for_strangles(strangles: list[Strangle]) -> dict[Option, float]:
    """
    Fetches the latest trading prices (LTPs) for a set of options extracted from a list of strangles.

    :param strangles: A list of Strangle objects.
    :return: A dictionary mapping each unique option to its latest trading price (LTP).
    """
    # Create a set of all distinct options from the strangles
    options = set(
        option
        for strangle in strangles
        for option in (strangle.call_option, strangle.put_option)
    )

    # Fetch the LTP for each unique option
    ltp_cache = {option: option.fetch_ltp() for option in options}
    return ltp_cache


def get_range_of_strangles(
    underlying: Index,
    underlying_ltp: float = None,
    call_strike_offset: float | int = 0,
    put_strike_offset: float | int = 0,
    expiry: str = None,
    strike_range: int = 3,
):
    underlying_ltp = (
        underlying.fetch_ltp() if underlying_ltp is None else underlying_ltp
    )

    if expiry is None:
        expiry = underlying.current_expiry

    if call_strike_offset == -put_strike_offset:  # Straddle
        strike = find_strike(underlying_ltp, underlying.base)
        strike_range = extend_strike_range(strike, underlying.base, strike_range)
        return [Straddle(strike, underlying.name, expiry) for strike in strike_range]
    else:
        call_strike = find_strike_with_offset(
            underlying_ltp, call_strike_offset, underlying.base
        )
        put_strike = find_strike_with_offset(
            underlying_ltp, -put_strike_offset, underlying.base
        )
        call_strike_range = extend_strike_range(
            call_strike, underlying.base, strike_range
        )
        put_strike_range = extend_strike_range(
            put_strike, underlying.base, strike_range
        )
        pairs = product(call_strike_range, put_strike_range)
        return [Strangle(pair[0], pair[1], underlying.name, expiry) for pair in pairs]


def most_equal_strangle(
    underlying: Index,
    call_strike_offset: float | int = 0,
    put_strike_offset: float | int = 0,
    disparity_threshold: float = 1000,
    exit_time: tuple[int, int] = (15, 25),
    range_of_strikes: int = 4,
    expiry: str = None,
    notification_url: str = None,
) -> Strangle | Straddle | None:
    if expiry is None:
        expiry = underlying.current_expiry

    strangles = get_range_of_strangles(
        underlying,
        call_strike_offset=call_strike_offset,
        put_strike_offset=put_strike_offset,
        expiry=expiry,
        strike_range=range_of_strikes,
    )
    # logger.info(f"{underlying.name} prospective strangles: {strangles}")

    # Define the price disparity function
    def price_disparity(strangle):
        call_ltp = ltp_cache[strangle.call_option]
        put_ltp = ltp_cache[strangle.put_option]
        return abs(call_ltp - put_ltp) / min(call_ltp, put_ltp)

    tracked_strangle = None

    last_notified_time = current_time() - timedelta(minutes=6)
    while current_time().time() < time(*exit_time):
        # If there's no tracked strangle update all prices and find the most equal strangle
        if tracked_strangle is None:
            ltp_cache = efficient_ltp_for_strangles(strangles)
            most_equal, min_disparity = min(
                ((s, price_disparity(s)) for s in strangles), key=lambda x: x[1]
            )
            if min_disparity < 0.10:
                tracked_strangle = most_equal

        # If there's a tracked strangle, check its disparity
        else:
            ltp_cache = {
                tracked_strangle.call_option: tracked_strangle.call_option.fetch_ltp(),
                tracked_strangle.put_option: tracked_strangle.put_option.fetch_ltp(),
            }
            most_equal = tracked_strangle
            min_disparity = price_disparity(tracked_strangle)
            if min_disparity >= 0.10:
                tracked_strangle = None

        logger.info(
            f"Most equal strangle: {most_equal} with disparity {min_disparity} "
            f"and prices {ltp_cache[most_equal.call_option]} and {ltp_cache[most_equal.put_option]}"
        )
        if last_notified_time < current_time() - timedelta(minutes=5):
            notifier(
                f"Most equal strangle: {most_equal} with disparity {min_disparity} "
                f"and prices {ltp_cache[most_equal.call_option]} and {ltp_cache[most_equal.put_option]}",
                notification_url,
                "INFO",
            )
            logger.info(f"Most equal ltp cache: {ltp_cache}")
            last_notified_time = current_time()
        # If the lowest disparity is below the threshold, return the most equal strangle
        if min_disparity < disparity_threshold:
            return most_equal
        else:
            pass
        sleep(0.5)

    else:
        return None


def most_even_strangle(
    underlying: Index,
    call_strike_offset: float | int = 0,
    put_strike_offset: float | int = 0,
    expiry: str = None,
) -> tuple[Strangle | Straddle, float] | tuple[None, np.nan]:
    strangle_deltas: dict = efficient_deltas_of_strangles(
        underlying, call_strike_offset, put_strike_offset, expiry
    )
    unevenness: dict = calculate_unevenness_of_deltas(strangle_deltas)
    target_strangle: Strangle | Straddle = min(unevenness, key=unevenness.get)
    minimum_unevenness: float = unevenness[target_strangle]
    if np.isnan(minimum_unevenness):
        return None, np.nan
    return target_strangle, minimum_unevenness


def efficient_deltas_of_strangles(
    underlying: Index,
    call_strike_offset: float | int = 0,
    put_strike_offset: float | int = 0,
    expiry: str = None,
    strike_range: int = 3,
) -> dict[Strangle, tuple[float, float]]:
    if expiry is None:
        expiry = underlying.current_expiry

    underlying_ltp = underlying.fetch_ltp()
    tte = time_to_expiry(expiry)

    prospective_strangles = get_range_of_strangles(
        underlying,
        underlying_ltp=underlying_ltp,
        call_strike_offset=call_strike_offset,
        put_strike_offset=put_strike_offset,
        expiry=expiry,
        strike_range=strike_range,
    )

    option_prices = efficient_ltp_for_strangles(prospective_strangles)
    option_greeks = {
        option: option.fetch_greeks(
            spot=underlying_ltp, price=option_prices[option], t=tte
        )
        for option in option_prices
    }

    strangle_deltas = {
        strangle: (
            option_greeks[strangle.call_option].delta,
            option_greeks[strangle.put_option].delta,
        )
        for strangle in prospective_strangles
    }

    return strangle_deltas


def calculate_unevenness_of_deltas(
    deltas: dict[Strangle, tuple[float, float]],
) -> dict[Strangle, float]:
    return {
        strangle: (max(np.abs(deltas[strangle])) / min(np.abs(deltas[strangle])))
        for strangle in deltas
    }


def load_current_straddle(
    underlying_str, user_id: str, file_appendix: str
) -> Straddle | None:
    """Load current position for a given underlying, user and strategy (file_appendix)."""

    # Loading current position
    trade_data = load_json_data(
        f"{user_id}\\{underlying_str}_{file_appendix}.json",
        default_structure=dict,
    )
    trade_data = trade_data.get(underlying_str, {})
    buy_strike = trade_data.get("strike", None)
    buy_expiry = trade_data.get("expiry", None)
    buy_straddle = (
        Straddle(strike=buy_strike, underlying=underlying_str, expiry=buy_expiry)
        if buy_strike is not None and buy_expiry is not None
        else None
    )
    return buy_straddle


def round_shares_to_lot_size(shares, lot_size):
    number = lot_size * round(shares / lot_size)
    return int(number)
