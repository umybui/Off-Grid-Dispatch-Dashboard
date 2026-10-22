import plotly.graph_objects as go


def build_peak_hour_share_chart(
    peak_snapshot
):

    # -------------------------------------
    # UNIT LEVEL
    # -------------------------------------

    if "Unit" in peak_snapshot.columns:

        fig = go.Figure()

        units = (
            peak_snapshot["Unit"]
            .astype(str)
            .unique()
        )

        for unit in units:

            temp = (
                peak_snapshot[
                    peak_snapshot["Unit"]
                    .astype(str)
                    == unit
                ]
            )

            fig.add_trace(
                go.Bar(
                    y=temp["Plant"],
                    x=temp[
                        "PeakEnergySharePct"
                    ],
                    orientation="h",
                    name=str(unit)
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
                x=plant_totals[
                    "PlantSharePct"
                ],
                y=plant_totals[
                    "Plant"
                ],
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
                "Peak Hour Energy "
                "Contribution Share"
            ),
            xaxis_title=
                "Peak Energy Share (%)",
            yaxis_title=
                "Plant",
            height=700,
            legend_title=
                "Plant | Unit"
        )

        fig.update_yaxes(
            categoryorder=
                "total ascending"
        )

        return fig

    # -------------------------------------
    # PLANT LEVEL
    # -------------------------------------

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

        height=650,

        yaxis=dict(
            categoryorder=
                "total ascending"
        )
    )

    return fig
