import pandas as pd

def build_reserve_dashboard(
    reserve
):

    reserve_df = reserve["reserve_df"]

    total_hours = len(
        reserve_df
    )

    unserved_hours = (
        reserve_df["ShortageMW"] > 0
    ).sum()

    served_hours = (
        total_hours
        - unserved_hours
    )

    adequate_hours = (
        reserve_df["ReserveCompliant"]
    ).sum()

    reserve_deficient_hours = (
        served_hours
        - adequate_hours
    )

    worst_reserve_deficiency = (
        reserve_df[
            "ReserveDeficiency"
        ].min()
    )

    return {

        "total_hours":
            total_hours,

        "unserved_hours":
            unserved_hours,

        "served_hours":
            served_hours,

        "adequate_hours":
            adequate_hours,

        "reserve_deficient_hours":
            reserve_deficient_hours,

        "worst_reserve_deficiency":
            worst_reserve_deficiency,

        "reserve_df":
            reserve_df
    }
