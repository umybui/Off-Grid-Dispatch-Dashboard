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

    chart_df = (
        unit_capability.copy()
    )

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
        chart_df["RiskFlag"]
        .dropna()
        .unique()
    ):

        temp = chart_df[
            chart_df["RiskFlag"]
            == flag
        ]

        fig.add_trace(
            go.Bar(
                y=temp[y_col],
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
            y_col,

        height=max(
            700,
            len(chart_df) * 25
        ),

        barmode="group"
    )

    return fig
