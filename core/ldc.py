import pandas as pd


def build_ldc(
    total_demand
):

    ldc = (
        total_demand[["Value"]]
        .rename(
            columns={
                "Value": "DemandMW"
            }
        )
        .copy()
    )

    ldc = ldc.sort_values(
        "DemandMW",
        ascending=False
    ).reset_index(
        drop=True
    )

    ldc["HourRank"] = (
        ldc.index + 1
    )

    ldc["Percentile"] = (
        ldc["HourRank"]
        /
        len(ldc)
        * 100
    )

    return ldc
