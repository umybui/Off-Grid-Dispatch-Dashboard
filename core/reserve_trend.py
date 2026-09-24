import pandas as pd
import plotly.graph_objects as go


def build_reserve_trend(
    reliability
):

    gap_df = (
        reliability["gap_df"]
        .copy()
    )

    gap_df["Month"] = (
        gap_df["Datetime"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    gap_df["MonthLabel"] = (
        gap_df["Datetime"]
        .dt.strftime("%b %Y")
    )

    gap_df["ServedFlag"] = (
        gap_df["ShortageMW"] <= 0
    )

    gap_df["ReserveCompliant"] = (
        (
            gap_df["ReserveMargin"]
            >=
            gap_df["RequiredReserve"]
        )
        &
        gap_df["ServedFlag"]
    )

    monthly = (
        gap_df
        .groupby(
            ["Month", "MonthLabel"],
            as_index=False
        )
        .agg(
            ServedHours=(
                "ServedFlag",
                "sum"
            ),

            CompliantHours=(
                "ReserveCompliant",
                "sum"
            )
        )
    )

    monthly["ReserveCompliancePct"] = (
        monthly["CompliantHours"]
        /
        monthly["ServedHours"]
        .replace(0, pd.NA)
        * 100
    )

    monthly = (
        monthly
        .sort_values("Month")
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["MonthLabel"],
            y=monthly[
                "ReserveCompliancePct"
            ],
            mode="lines+markers+text",

            text=(
                monthly[
                    "ReserveCompliancePct"
                ]
                .round(1)
                .astype(str)
                + "%"
            ),

            textposition=
                "top center"
        )
    )

    fig.add_hline(
        y=95,
        line_dash="dash",
        line_color="green",
        annotation_text="Excellent"
    )

    fig.add_hline(
        y=90,
        line_dash="dot",
        line_color="gold",
        annotation_text="Good"
    )

    fig.add_hline(
        y=80,
        line_dash="dot",
        line_color="orange",
        annotation_text="Fair"
    )

    fig.update_layout(
        title=
            "Monthly Reserve Compliance Trend",

        xaxis_title="Month",

        yaxis_title=
            "Reserve Compliance (%)",

        yaxis=dict(
            range=[0, 100]
        ),

        height=450
    )

    return {
        "monthly":
            monthly,

        "figure":
            fig
    }
