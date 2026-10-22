import plotly.graph_objects as go


def get_shade(hex_color, factor):

    hex_color = hex_color.lstrip("#")

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = int(r * factor + 255 * (1 - factor))
    g = int(g * factor + 255 * (1 - factor))
    b = int(b * factor + 255 * (1 - factor))

    return f"#{r:02X}{g:02X}{b:02X}"


def build_peak_hour_share_chart(
    peak_snapshot
):

    # ---------------------------------------------
    # FALLBACK TO PLANT-LEVEL IF NO UNIT COLUMN
    # ---------------------------------------------

    if "Unit" not in peak_snapshot.columns:

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

    # ---------------------------------------------
    # UNIT-LEVEL VERSION
    # ---------------------------------------------

    plant_share = (
        peak_snapshot[
            [
                "Plant",
                "PlantSharePct"
            ]
        ]
        .drop_duplicates()
    )

    plant_order = (
        plant_share
        .sort_values(
            "PlantSharePct",
            ascending=False
        )["Plant"]
        .tolist()
    )

    plant_base_colors = {
        "E-DELTA P": "#1565C0",
        "TDELTA P": "#FB8C00",
        "DMCI ABORLAN": "#2E7D32",
        "DMCI NARRA": "#C62828",
        "DMCI IRAWAN": "#6A1B9A",
        "DMCI QUEZON": "#00897B",
        "DMCI RIO TUBA": "#283593",
        "VPOWER": "#616161",
        "DMCI IRAWAN EPSA": "#8D6E63"
    }

    fig = go.Figure()

    for plant in plant_order:

        plant_units = (
            peak_snapshot[
                peak_snapshot["Plant"]
                == plant
            ]
            .sort_values(
                "PeakEnergySharePct",
                ascending=False
            )
        )

        if plant_units.empty:
            continue

        base_color = (
            plant_base_colors.get(
                str(plant).upper(),
                "#1565C0"
            )
        )

        unit_count = max(
            len(plant_units),
            2
        )

        shade_levels = [
            1.00
            -
            (
                (1.00 - 0.25)
                * i
                / (unit_count - 1)
            )
            for i in range(unit_count)
        ]

        for idx, (_, row) in enumerate(
            plant_units.iterrows()
        ):

            color = get_shade(
                base_color,
                shade_levels[idx]
            )

            fig.add_trace(
                go.Bar(
                    y=[row["Plant"]],
                    x=[
                        row[
                            "PeakEnergySharePct"
                        ]
                    ],
                    orientation="h",
                    marker_color=color,
                    name=row["Plant"],
                    showlegend=(idx == 0),
                    hovertemplate=
                        f"<b>{row['Plant']}</b><br>"
                        f"Unit: {row['Unit']}<br>"
                        "Contribution: %{x:.2f}%"
                        "<extra></extra>"
                )
            )

    for _, row in (
        plant_share.iterrows()
    ):

        fig.add_annotation(
            x=row["PlantSharePct"],
            y=row["Plant"],
            text=(
                f"{row['PlantSharePct']:.1f}%"
            ),
            showarrow=False,
            xanchor="left"
        )

    fig.update_layout(
        barmode="stack",
        title=(
            "Peak Hour Energy Contribution Share"
        ),
        xaxis_title=
            "Share of Total Peak-Hour Energy (%)",
        yaxis_title=
            "Plant",
        height=max(
            550,
            len(plant_order) * 45
        ),
        legend_title="Plant | Unit"
    )

    fig.update_yaxes(
        categoryorder="array",
        categoryarray=plant_order[::-1]
    )

    return fig
