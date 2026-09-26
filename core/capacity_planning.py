import pandas as pd


def build_capacity_planning(
    reliability,
    capacity_reference,
    growth_rate=3.0
):

    peak_demand = (
        reliability["peak_demand"]
    )

    planning_horizon = 10

    available_capacity = (
        capacity_reference[
            "DependableMW"
        ].sum()
        if len(capacity_reference) > 0
        else 0
    )

    projected_peak = (
        peak_demand
        * (1 + growth_rate / 100)
        ** planning_horizon
    )

    capacity_margin = (
        available_capacity
        - projected_peak
    )

    reserve_margin_pct = (
        capacity_margin
        / projected_peak
        * 100
        if projected_peak > 0
        else 0
    )

    required_capacity = max(
        projected_peak
        - available_capacity,
        0
    )

    projection_rows = []

    for yr in range(0, 11):

        projected = (
            peak_demand
            * (1 + growth_rate / 100)
            ** yr
        )

        margin = (
            available_capacity
            - projected
        )

        projection_rows.append(
            {
                "Year Ahead": yr,

                "Projected Peak MW":
                    round(
                        projected,
                        2
                    ),

                "Capacity Margin MW":
                    round(
                        margin,
                        2
                    ),

                "Additional Capacity Needed MW":
                    round(
                        max(
                            -margin,
                            0
                        ),
                        2
                    )
            }
        )

    projection_df = pd.DataFrame(
        projection_rows
    )

    return {

        "peak_demand":
            peak_demand,

        "projected_peak":
            projected_peak,

        "available_capacity":
            available_capacity,

        "capacity_margin":
            capacity_margin,

        "reserve_margin_pct":
            reserve_margin_pct,

        "required_capacity":
            required_capacity,

        "projection_df":
            projection_df
    }
``
