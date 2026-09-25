import pandas as pd


def build_reserve_deficiency_table(
    reliability
):

    reserve_detail = (
        reliability["gap_df"]
        .copy()
    )

    reserve_detail = reserve_detail[
        reserve_detail["ShortageMW"] <= 0
    ]

    reserve_detail = reserve_detail[
        reserve_detail["ReserveMargin"]
        <
        reserve_detail["RequiredReserve"]
    ]

    reserve_detail[
        "ReserveDeficiency"
    ] = (
        reserve_detail["ReserveMargin"]
        -
        reserve_detail["RequiredReserve"]
    )

    reserve_detail = (
        reserve_detail
        .sort_values(
            "ReserveDeficiency",
            ascending=True
        )
        .reset_index(drop=True)
    )

    reserve_detail.insert(
        0,
        "Rank",
        range(
            1,
            len(reserve_detail) + 1
        )
    )

    reserve_detail = reserve_detail[
        [
            "Rank",
            "Datetime",
            "TotalDemand",
            "TotalSupply",
            "ReserveMargin",
            "RequiredReserve",
            "ReserveDeficiency"
        ]
    ]

    return reserve_detail
