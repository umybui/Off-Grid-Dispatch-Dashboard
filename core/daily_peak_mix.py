import pandas as pd
import plotly.graph_objects as go


def build_daily_peak_mix(
    total_demand,
    generation,
    capacity_reference
):

    demand = total_demand.copy()

    demand["Date"] = (
        demand["Datetime"]
        .dt.date
    )

    daily_peak_hours = (
        demand
        .sort_values(
            "Value",
            ascending=False
        )
        .groupby(
            "Date",
            as_index=False
        )
        .first()
    )

    peak_datetimes = (
        daily_peak_hours[
            "Datetime"
        ]
    )

    daily_generation = (
        generation[
            generation["Datetime"]
            .isin(
                peak_datetimes
            )
        ]
        .copy()
    )

    total_daily_peak = (
        daily_generation
        .groupby(
            "Datetime"
        )["Value"]
        .transform(
            "sum"
        )
    )

    daily_generation[
        "SharePct"
    ] = (
        daily_generation["Value"]
        /
        total_daily_peak
        * 100
    )

    daily_generation["Date"] = (
        daily_generation["Datetime"]
        .dt.date
    )

    fig = go.Figure()

    plant_order = (
        daily_generation
        .groupby(
            "Plant"
        )["Value"]
        .sum()
        .sort_values(
            ascending=False
        )
        .index
        .tolist()
    )

    for plant in plant_order:

        temp = (
            daily_generation[
                daily_generation["Plant"]
                == plant
            ]
        )

        fig.add_trace(
            go.Bar(
                x=temp["Date"],
                y=temp["SharePct"],
                name=plant
            )
        )

    fig.update_layout(
        barmode="stack",
        height=650,
        title=(
            "Generation Mix During Daily System Peaks"
        ),
        yaxis_title="Share (%)",
        xaxis_title="Date"
    )

    performance_table = (
        daily_generation
        .groupby(
            "Plant",
            as_index=False
        )
        .agg(
            AvgPeakMW=(
                "Value",
                "mean"
            ),
            MaxPeakMW=(
                "Value",
                "max"
            )
        )
    )

    if (
        len(capacity_reference)
        > 0
    ):

        performance_table = (
            performance_table
            .merge(
                capacity_reference[
                    [
                        "Plant",
                        "DependableMW",
                        "AvailableMW"
                    ]
                ],
                on="Plant",
                how="left"
            )
        )

        performance_table[
            "PeakSupportPct"
        ] = (
            performance_table[
                "MaxPeakMW"
            ]
            /
            performance_table[
                "DependableMW"
            ].clip(
                lower=0.01
            )
            * 100
        )

        performance_table[
            "RiskFlag"
        ] = (
            performance_table[
                "PeakSupportPct"
            ]
            .apply(
                lambda x:
                "OK"
                if x >= 90
                else (
                    "Monitor"
                    if x >= 80
                    else
                    "Underperforming"
                )
            )
        )

        performance_table[
            "Remarks"
        ] = (
            performance_table[
                "RiskFlag"
            ]
            .map(
                {
                    "OK":
                    "Unit achieved expected capability during peak-demand periods.",

                    "Monitor":
                    "Below full capability during peak conditions.",

                    "Underperforming":
                    "Significant shortfall during peak-demand periods."
                }
            )
        )

    return {

        "figure":
            fig,

        "performance_table":
            performance_table

    }
