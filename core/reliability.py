import pandas as pd

def build_reliability(
    total_demand,
    total_generation,
    transfer_flow
):

    gap_df = total_demand.merge(
        total_generation,
        on="Datetime",
        how="inner"
    )

    gap_df.rename(
        columns={
            "Value": "TotalDemand"
        },
        inplace=True
    )

    if transfer_flow.empty:

        gap_df["ImportSupport"] = 0

    else:

        gap_df = gap_df.merge(
            transfer_flow,
            on="Datetime",
            how="left"
        )

        gap_df["ImportSupport"] = (
            gap_df["ImportSupport"]
            .fillna(0)
        )

    gap_df["TotalSupply"] = (
        gap_df["TotalGeneration"]
        +
        gap_df["ImportSupport"]
    )

    SHORTAGE_THRESHOLD = 0.01

    gap_df["ShortageMW"] = (
        gap_df["TotalDemand"]
        -
        gap_df["TotalSupply"]
    ).round(2)

    gap_df["ShortageArea"] = (
        gap_df["ShortageMW"]
        .clip(lower=0)
    )

    gap_df["ReserveMargin"] = (
        gap_df["TotalSupply"]
        -
        gap_df["TotalDemand"]
    )

    gap_df["RegulatingReserve"] = (
        gap_df["TotalDemand"] * 0.028
    )

    gap_df["ContingencyReserve"] = (
        gap_df["TotalGeneration"] * 0.10
    )

    gap_df["RequiredReserve"] = (
        gap_df["RegulatingReserve"]
        +
        gap_df["ContingencyReserve"]
    )

    peak_demand = (
        gap_df["TotalDemand"]
        .max()
    )

    peak_row = gap_df.loc[
        gap_df["TotalDemand"].idxmax()
    ]

    peak_datetime = peak_row["Datetime"]

    hours_with_shortage = (
        gap_df["ShortageMW"]
        >= SHORTAGE_THRESHOLD
    ).sum()

    max_shortage = max(
        gap_df["ShortageMW"].max(),
        0
    )

    unserved_energy = (
        gap_df.loc[
            gap_df["ShortageMW"]
            >= SHORTAGE_THRESHOLD,
            "ShortageMW"
        ]
        .sum()
    )

    hours_low_reserve = (
        gap_df["ReserveMargin"]
        <
        gap_df["RequiredReserve"]
    ).sum()

    total_shortage_mwh = (
        gap_df.loc[
            gap_df["ShortageMW"]
            >= SHORTAGE_THRESHOLD,
            "ShortageMW"
        ]
        .sum()
    )

    return {
        "gap_df": gap_df,
        "peak_demand": peak_demand,
        "peak_datetime": peak_datetime,
        "hours_with_shortage": hours_with_shortage,
        "max_shortage": max_shortage,
        "unserved_energy": unserved_energy,
        "hours_low_reserve": hours_low_reserve,
        "total_shortage_mwh": total_shortage_mwh
    }
