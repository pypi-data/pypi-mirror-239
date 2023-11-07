import pandas as pd
from datetime import timedelta


def update_positions_and_premium(
    row: pd.Series,
    net_delta: float,
    call_positions: int,
    put_positions: int,
    premium_received: float,
    delta_threshold: float,
) -> tuple[int, int, float]:
    if (
        net_delta > delta_threshold
    ):  # Net delta is positive, sell the required call amount to neutralize
        qty_call_to_sell = int((abs(net_delta) - 0) / row["call_deltas"])
        call_positions -= qty_call_to_sell
        premium_received += qty_call_to_sell * row["call_price"]
    elif (
        net_delta < -delta_threshold
    ):  # Net delta is negative, sell another put to neutralize
        qty_put_to_sell = int((abs(net_delta) - 0) / abs(row["put_deltas"]))
        put_positions -= qty_put_to_sell
        premium_received += qty_put_to_sell * row["put_price"]

    return call_positions, put_positions, premium_received


def process_segment(
    prepared_segment: pd.DataFrame,
    qty_to_trade: int,
    delta_interval_minutes: int,
    exit_qty: int,
) -> pd.DataFrame:
    entry_data = prepared_segment.iloc[0]
    call_positions = -qty_to_trade  # Sell call
    put_positions = -qty_to_trade  # Sell put
    premium_received = (
        entry_data["call_price"] * qty_to_trade + entry_data["put_price"] * qty_to_trade
    )  # Update PnL
    delta_check_interval = entry_data.name + timedelta(minutes=delta_interval_minutes)

    # Lists to store PnL and net delta for each minute
    premium_received_history = []
    net_delta_history = []
    call_position_history = []
    put_position_history = []
    mtm_history = []

    # Iterate through the data minute by minute
    for i, row in prepared_segment.iterrows():
        net_delta = (
            call_positions * row["call_deltas"] + put_positions * row["put_deltas"]
        )

        # Calculation of delta threshold
        one_min_std = 0.00035 * row["open"]
        position_gamma = row["call_gammas"] * abs(call_positions) + row[
            "put_gammas"
        ] * abs(put_positions)
        delta_threshold = one_min_std * position_gamma

        if abs(net_delta) > delta_threshold and i >= delta_check_interval:
            (
                call_positions,
                put_positions,
                premium_received,
            ) = update_positions_and_premium(
                row,
                net_delta,
                call_positions,
                put_positions,
                premium_received,
                delta_threshold,
            )

            # Update the net delta
            net_delta = (
                call_positions * row["call_deltas"] + put_positions * row["put_deltas"]
            )
            delta_check_interval = i + timedelta(minutes=delta_interval_minutes)

            if abs(call_positions) > exit_qty or abs(put_positions) > exit_qty:
                # Exit if max position size is reached
                # Make the final appends before breaking
                premium_received_history.append(premium_received)
                net_delta_history.append(net_delta)
                call_position_history.append(call_positions)
                put_position_history.append(put_positions)
                mtm_history.append(
                    call_positions * row["call_price"]
                    + put_positions * row["put_price"]
                )
                break

        # Append histories
        premium_received_history.append(premium_received)
        net_delta_history.append(net_delta)
        call_position_history.append(call_positions)
        put_position_history.append(put_positions)
        mtm_history.append(
            call_positions * row["call_price"] + put_positions * row["put_price"]
        )

    segment_result = pd.DataFrame(
        {
            "call_positions": call_position_history,
            "put_positions": put_position_history,
            "net_delta": net_delta_history,
            "premium": premium_received_history,
            "mtm": mtm_history,
        },
        index=prepared_segment[(prepared_segment.index <= i)].index,
    )

    return segment_result


def summarize_results(df: pd.DataFrame) -> pd.DataFrame:
    # Identify duplicate timestamps, which signify exit points
    duplicate_times = df[df.index.duplicated(keep="last")]

    # Finding the last row of each day
    final_exits = df.loc[
        df.groupby(df.index.date).apply(lambda x: x.iloc[-1].name).tolist()
    ]

    exit_times = pd.concat([duplicate_times, final_exits])

    # For each duplicate date, sum the 'premium' and 'mtm' to calculate profit
    exit_times["profit"] = exit_times["premium"] + exit_times["mtm"]

    return exit_times.sort_index()
