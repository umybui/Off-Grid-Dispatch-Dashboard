import plotly.graph_objects as go


def build_operating_condition_breakdown(
    reliability
):

    gap_df = reliability["gap_df"]

    total_hours = len(gap_df)

    shortage_hours = (
        gap_df["ShortageMW"] > 0
    ).sum()

    served_df = gap_df[
        gap_df["ShortageMW"] <= 0
    ].copy()

    adequate_hours = (
        served_df["ReserveMargin"]
        >= served_df["RequiredReserve"]
    ).sum()

    reserve_deficient_hours = (
        served_df["ReserveMargin"]
        < served_df["RequiredReserve"]
    ).sum()

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=["Study Period"],
            x=[adequate_hours],
            name="Adequate Reserve",
            orientation="h",
            marker_color="green",
            text=[f"{adequate_hours:,}"],
            textposition="inside"
        )
    )

    fig.add_trace(
        go.Bar(
            y=["Study Period"],
            x=[reserve_deficient_hours],
            name="Reserve Deficient",
            orientation="h",
            marker_color="orange",
            text=[f"{reserve_deficient_hours:,}"],
            textposition="inside"
        )
    )

    fig.add_trace(
        go.Bar(
            y=["Study Period"],
            x=[shortage_hours],
            name="Unserved Demand",
            orientation="h",
            marker_color="red",
            text=[f"{shortage_hours:,}"],
            textposition="inside"
        )
    )

    fig.update_layout(
        title="Operating Condition Breakdown",
        barmode="stack",
        xaxis_title="Hours",
        height=350
    )

    return {

        "adequate_hours":
            adequate_hours,

        "reserve_deficient_hours":
            reserve_deficient_hours,

        "shortage_hours":
            shortage_hours,

        "figure":
            fig
    }
