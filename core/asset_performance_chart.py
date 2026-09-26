import plotly.graph_objects as go


def build_asset_performance_chart(
    asset_performance
):

    color_map = {
        "OK": "green",
        "Monitor": "gold",
        "Underperforming": "red",
        "Unavailable": "gray",
        "No Data": "lightgray"
    }

    fig = go.Figure()

    for flag in (
        asset_performance["RiskFlag"]
        .dropna()
        .unique()
    ):

        temp = asset_performance[
            asset_performance["RiskFlag"]
            == flag
        ]

        fig.add_trace(
            go.Bar(
                y=temp["Plant"],
                x=temp[
                    "CapabilityRealizationPct"
                ],
                orientation="h",
                name=flag,
                marker_color=color_map.get(
                    flag,
                    "blue"
                )
            )
        )

    fig.add_vline(
        x=95,
        line_dash="dash",
        line_color="green"
    )

    fig.add_vline(
        x=75,
        line_dash="dash",
        line_color="orange"
    )

    fig.update_layout(
        title=
            "Capability Realization by Plant",

        xaxis_title=
            "Max Observed MW / Dependable MW (%)",

        yaxis_title=
            "Plant",

        height=max(
            650,
            len(asset_performance) * 35
        ),

        barmode="group"
    )

    return fig
