import plotly.graph_objects as go


def build_unit_capability_chart(
    unit_capability
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
        unit_capability["RiskFlag"]
        .dropna()
        .unique()
    ):

        temp = unit_capability[
            unit_capability["RiskFlag"]
            == flag
        ]

        fig.add_trace(
            go.Bar(
                y=temp["Plant"],
                x=temp[
                    "SustainedCapabilityPct"
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
        x=80,
        line_dash="dash",
        line_color="green"
    )

    fig.add_vline(
        x=40,
        line_dash="dash",
        line_color="orange"
    )

    fig.update_layout(
        title=
            "Unit Sustained Capability Assessment",

        xaxis_title=
            "% of Operating Hours Above 80% Dependable Capacity",

        yaxis_title=
            "Plant",

        height=max(
            700,
            len(unit_capability) * 30
        ),

        barmode="group"
    )

    return fig
