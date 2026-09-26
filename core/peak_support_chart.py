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

    fig = go.Figure()

    for flag in (
        peak_support[
            "RiskFlag"
        ]
        .dropna()
        .unique()
    ):

        temp = peak_support[
            peak_support[
                "RiskFlag"
            ] == flag
        ]

        fig.add_trace(

            go.Bar(
                y=temp["Plant"],

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
            "Plant",

        height=max(
            600,
            len(peak_support) * 35
        ),

        barmode="group"
    )

    return fig
