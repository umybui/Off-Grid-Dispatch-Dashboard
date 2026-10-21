import plotly.graph_objects as go


def build_peak_hour_share_chart(
    peak_snapshot
):

    fig = go.Figure()

    plants = (
        peak_snapshot["Plant"]
        .drop_duplicates()
        .tolist()
    )

    for unit in peak_snapshot["Unit"].astype(str).unique():

        temp = peak_snapshot[
            peak_snapshot["Unit"]
            .astype(str)
            == unit
        ]

        fig.add_trace(
            go.Bar(
                y=temp["Plant"],
                x=temp["PeakEnergySharePct"],
                orientation="h",
                name=unit
            )
        )

    plant_totals = (
        peak_snapshot[
            [
                "Plant",
                "PlantSharePct"
            ]
        ]
        .drop_duplicates()
    )

    fig.add_trace(
        go.Scatter(
            x=plant_totals["PlantSharePct"],
            y=plant_totals["Plant"],
            mode="text",
            text=[
                f"{v:.1f}%"
                for v in plant_totals[
                    "PlantSharePct"
                ]
            ],
            textposition="middle right",
            showlegend=False
        )
    )

    fig.update_layout(
        barmode="stack",
        title=(
            "Peak Hour Energy Contribution Share "
            "(90%-100% of Peak Demand)"
        ),
        xaxis_title=(
            "Share of Total Peak-Hour Energy (%)"
        ),
        yaxis_title="Plant",
        height=700,
        legend_title="Plant | Unit"
    )

    fig.update_yaxes(
        categoryorder="total ascending"
    )

    return fig
