import plotly.graph_objects as go


def build_peak_hour_share_chart(
    peak_snapshot
):

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=peak_snapshot["Plant"],
            x=peak_snapshot[
                "PeakEnergySharePct"
            ],
            orientation="h",

            text=(
                peak_snapshot[
                    "PeakEnergySharePct"
                ]
                .round(1)
            ),

            texttemplate="%{text:.1f}%",

            textposition="outside"
        )
    )

    fig.update_layout(

        title=(
            "Peak Hour Energy "
            "Contribution Share"
        ),

        xaxis_title=
            "Peak Energy Share (%)",

        yaxis_title=
            "Plant",

        height=600,

        yaxis=dict(
            categoryorder=
                "total ascending"
        )
    )

    return fig
