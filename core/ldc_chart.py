import plotly.graph_objects as go


def get_segment_name(
    i,
    total_segments
):

    if total_segments == 1:
        return "Load"

    if i == 0:
        return "Peaking"

    if i == total_segments - 1:
        return "Baseload"

    if total_segments == 3:
        return "Mid-Merit"

    return f"Mid-Merit {i}"


def build_ldc_chart(
    ldc,
    boundaries,
    compressed_points
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ldc["Percentile"],
            y=ldc["DemandMW"],
            mode="lines",
            name="Demand",
            line=dict(
                color="black",
                width=3
            )
        )
    )

    segment_colors = [
        "red",
        "orange",
        "gold",
        "green",
        "deepskyblue",
        "mediumpurple",
        "gray",
        "brown"
    ]

    scale_factor = (
        len(ldc)
        /
        compressed_points
    )

    summary_rows = []

    for i, (
        start_idx,
        end_idx
    ) in enumerate(boundaries):

        actual_start = int(
            start_idx * scale_factor
        )

        actual_end = int(
            end_idx * scale_factor
        )

        segment_data = ldc.iloc[
            actual_start:actual_end
        ]

        if len(segment_data) == 0:
            continue

        segment_max = (
            segment_data["DemandMW"]
            .max()
        )

        segment_min = (
            segment_data["DemandMW"]
            .min()
        )

        start_pct = (
            actual_start
            /
            len(ldc)
            * 100
        )

        end_pct = (
            actual_end
            /
            len(ldc)
            * 100
        )

        duration_pct = (
            end_pct
            - start_pct
        )

        segment_name = (
            get_segment_name(
                i,
                len(boundaries)
            )
        )

        fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    size=10,
                    color=segment_colors[
                        i % len(segment_colors)
                    ]
                ),
                name=segment_name
            )
        )
        
        fig.add_vrect(
            x0=start_pct,
            x1=end_pct,
            fillcolor=segment_colors[
                i %
                len(segment_colors)
            ],
            opacity=0.12,
            line_width=0
        )

        fig.add_vline(
            x=end_pct,
            line_dash="dot",
            line_color="black"
        )

        fig.add_annotation(
            x=(
                start_pct
                + end_pct
            ) / 2,
            y=segment_max,
            text=(
                f"<b>{segment_name}</b><br>"
                f"{segment_max:.1f} - "
                f"{segment_min:.1f} MW<br>"
                f"{duration_pct:.1f}%"
            ),
            showarrow=False,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1,
            opacity=0.9
        )

        summary_rows.append(
            {
                "Segment":
                    segment_name,

                "MW Range":
                    f"{segment_max:.2f} - {segment_min:.2f}",

                "Duration %":
                    round(
                        duration_pct,
                        2
                    )
            }
        )

        transition_x = end_pct
        
        transition_y = segment_min
        
        marker_color = (
            "red"
            if i == 0
            else
            "green"
            if i == len(boundaries) - 1
            else
            "orange"
        )
        
        fig.add_trace(
            go.Scatter(
                x=[transition_x],
                y=[transition_y],
                mode="markers",
                marker=dict(
                    size=8,
                    color=marker_color
                ),
                showlegend=False
            )
        )
    
    average_load = (
        ldc["DemandMW"]
        .mean()
    )

    fig.add_hline(
        y=average_load,
        line_dash="dash",
        annotation_text=
            f"Average Load ({average_load:.2f} MW)"
    )

    peak_load = (
    ldc["DemandMW"]
    .max()
    )
    
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[peak_load],
            mode="markers",
            marker=dict(
                color="red",
                size=10
            ),
            showlegend=False
        )
    )

    fig.add_annotation(
        x=0,
        y=peak_load,
        text=(
            "Peak Demand<br>"
            f"{ldc['DemandMW'].max():.2f} MW"
        ),
        showarrow=True
    )

    base_load = (
    ldc["DemandMW"]
    .min()
    )
    
    fig.add_trace(
        go.Scatter(
            x=[100],
            y=[base_load],
            mode="markers",
            marker=dict(
                color="green",
                size=10
            ),
            showlegend=False
        )
    )

    fig.add_annotation(
        x=100,
        y=base_load,
        text=(
            "Minimum Demand<br>"
            f"{ldc['DemandMW'].min():.2f} MW"
        ),
        showarrow=True
    )

    fig.update_layout(
        legend_title="Segment",
        legend=dict(
            orientation="v"
        ),
        title=(
        f"Load Duration Curve "
        f"({len(boundaries)} Segments)"
        ),
        xaxis_title="Percent of Time Exceeded (%)",
        yaxis_title="Demand (MW)",
        hovermode="x unified",
        height=650
    )

    return fig, summary_rows
