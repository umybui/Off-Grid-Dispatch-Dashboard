import plotly.graph_objects as go


def build_peak_support_chart(
    peak_support
):

    color_map = {

        "OK":
            "green",

        "Monitor":
            "gold",

        "Underperforming":
            "red",

        "Unavailable":
            "gray",

        "No Data":
            "lightgray"
    }

    chart_df = peak_support.copy()

    if "Unit" in chart_df.columns:

        chart_df["PlantUnit"] = (
            chart_df["Plant"]
            + " | "
            + chart_df["Unit"].astype(str)
        )

        y_col = "PlantUnit"

    else:

        y_col = "Plant"

    fig = go.Figure()

    for flag in (
        chart_df[
            "RiskFlag"
        ]
        .dropna()
        .unique()
    ):

        temp = chart_df[
            chart_df[
                "RiskFlag"
            ] == flag
        ]

        fig.add_trace(

            go.Bar(
                y=temp[y_col],

                x=temp[
                    "PeakSupportPct"
                ],

                orientation="h",

                name=flag,

                marker_color=
                    color_map.get(
                        flag,
                        "blue"
                    )
            )
        )

    fig.add_vline(
        x=90,
        line_dash="dash",
        line_color="green"
    )

    fig.add_vline(
        x=70,
        line_dash="dash",
        line_color="orange"
    )

    fig.update_layout(

        title=(
            "Peak Support "
            "Achievement Chart"
        ),

        xaxis_title=
            "Peak Support (%)",

        yaxis_title=
            y_col,

        height=max(
            600,
            len(chart_df) * 25
        ),

        barmode="group"
    )

    return fig
