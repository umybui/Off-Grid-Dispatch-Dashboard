import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def build_reliability_monitor(
    reliability,
    kpis
):

    st.subheader(
        "Reliability Health Monitor"
    )

    st.caption(
        "The three weights must total exactly 100%."
    )
    
    # =====================================================
    # User Weights
    # =====================================================

    w1, w2, w3 = st.columns(3)
    
    with w1:
    
        unserved_weight = st.number_input(
            "Unserved Energy Weight (%)",
            min_value=0,
            max_value=100,
            value=50,
            step=5
        )
    
    with w2:
    
        shortage_weight = st.number_input(
            "Shortage Hours Weight (%)",
            min_value=0,
            max_value=100,
            value=25,
            step=5
        )
    
    with w3:
    
        reserve_weight = st.number_input(
            "Low Reserve Hours Weight (%)",
            min_value=0,
            max_value=100,
            value=25,
            step=5
        )


    # =====================================================
    # Validation
    # =====================================================

    weight_total = (
        unserved_weight
        + shortage_weight
        + reserve_weight
    )
    
    if weight_total != 100:
    
        st.error(
            f"Weight Total = {weight_total}% "
            f"(must equal 100%)"
        )
    
    else:
    
        st.success(
            "✓ Weight Total = 100%"
        )

    # =====================================================
    # Score
    # =====================================================

    unserved_penalty = min(
        reliability["unserved_energy"] /
        max(
            kpis["demand_energy_mwh"],
            1
        ),
        1
    )
    
    shortage_penalty = min(
        reliability["hours_with_shortage"] /
        len(reliability["gap_df"]),
        1
    )
    
    reserve_penalty = min(
        reliability["hours_low_reserve"] /
        len(reliability["gap_df"]),
        1
    )

    reliability_score = 100 - (
    
        unserved_penalty
        *
        unserved_weight
    
        +
    
        shortage_penalty
        *
        shortage_weight
    
        +
    
        reserve_penalty
        *
        reserve_weight
    
    )
    #Create limit    
    reliability_score = max(
        0,
        min(100, reliability_score)
    )

    # =====================================================
    # Status
    # =====================================================

    if reliability_score >= 85:
    
        health_status = "Excellent"
    
    elif reliability_score >= 70:
    
        health_status = "Good"
    
    elif reliability_score >= 50:
    
        health_status = "Fair"
    
    else:
    
        health_status = "Poor"

    # =====================================================
    # KPI Cards
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
    
        st.metric(
            "Study Period Reliability Score",
            f"{reliability_score:.0f}/100"
        )
    
    with c2:
    
        st.metric(
            "Study Period Unserved Energy",
            f"{reliability['unserved_energy']:,.1f} MWh"
        )
    
    with c3:
    
        reserve_adequacy = 100 * (
            1
            -
            (
                reliability["hours_low_reserve"]
                /
                len(reliability["gap_df"])
            )
        )
    
        st.metric(
            "Study Period Reserve Adequacy",
            f"{reserve_adequacy:.1f}%"
        )
    
    with c4:
    
        st.metric(
            "Study Period Low Reserve Hours",
            reliability["hours_low_reserve"]
        )

    st.caption(
        """
        Study Period Reliability Score is evaluated over the
        entire selected analysis period.
    
        Score Formula:
    
        Reliability Score =
        100 − (
            Unserved Energy Penalty × Weight
            + Shortage Hours Penalty × Weight
            + Low Reserve Hours Penalty × Weight
        )
    
        Where:
    
        • Unserved Energy Penalty =
          Unserved Energy ÷ Demand Energy
    
        • Shortage Hours Penalty =
          Hours with Shortage ÷ Total Hours
    
        • Low Reserve Hours Penalty =
          Low Reserve Hours ÷ Total Hours
    
        Default Weights:
    
        • Unserved Energy = 50%
        • Shortage Hours = 25%
        • Low Reserve Hours = 25%
    
        Higher scores indicate better overall reliability.
        """
    )
    
    # =====================================================
    # MONTH-BY-MONTH TRAFFIC LIGHTS
    # =====================================================
    
    monthly_gap = (
        reliability["gap_df"]
        .copy()
    )
    
    monthly_gap["Month"] = (
        monthly_gap["Datetime"]
        .dt.strftime("%b %Y")
    )
    
    monthly_gap["MonthSort"] = (
        monthly_gap["Datetime"]
        .dt.to_period("M")
    )
    
    monthly_status = (
        monthly_gap
        .groupby(
            ["Month", "MonthSort"]
        )
        .agg(
            UnservedEnergy=(
                "ShortageMW",
                "sum"
            ),
            ShortageHours=(
                "ShortageMW",
                lambda x: (x > 0).sum()
            )
        )
        .reset_index()
        .sort_values(
            "MonthSort"
        )
    )
    
    traffic = []
    
    for _, row in monthly_status.iterrows():
    
        if row["ShortageHours"] == 0:
    
            traffic.append("🟢")
    
        elif row["ShortageHours"] < 24:
    
            traffic.append("🟡")
    
        elif row["ShortageHours"] < 72:
    
            traffic.append("🟠")
    
        else:
    
            traffic.append("🔴")
    
    st.markdown(
        " ".join(
            [
                f"{month} {icon}"
                for month, icon in zip(
                    monthly_status["Month"],
                    traffic
                )
            ]
        )
    )

    st.caption(
        """
        Traffic Light Legend:
    
        🟢 Excellent (Score ≥ 85) |
        🟡 Good (70-84) |
        🟠 Fair (50-69) |
        🔴 Poor (<50)
        """
    )
    
    # =====================================================
    # MONTHLY UNSERVED ENERGY TREND
    # =====================================================
    
    monthly_unserved = (
        monthly_gap
        .groupby(
            ["Month", "MonthSort"]
        )["ShortageMW"]
        .sum()
        .reset_index()
        .sort_values(
            "MonthSort"
        )
    )

    #color logic
    bar_colors = []
    
    for value in monthly_unserved["ShortageMW"]:
    
        if value < 100:
    
            bar_colors.append("#4CAF50")
    
        elif value < 500:
    
            bar_colors.append("#FB8C00")
    
        else:
    
            bar_colors.append("#C62828")

    #cxhart
    fig_unserved = go.Figure()
    
    fig_unserved.add_trace(
        go.Bar(
            x=monthly_unserved["Month"],
            y=monthly_unserved["ShortageMW"],
            marker_color=bar_colors,
            text=monthly_unserved["ShortageMW"].round(1),
            textposition="outside"
        )
    )
    
    fig_unserved.update_layout(
        title="Monthly Unserved Energy Trend",
        yaxis_title="Unserved Energy (MWh)",
        xaxis_title="Month",
        height=400
    )
    
    st.plotly_chart(
        fig_unserved,
        use_container_width=True
    )

    # =====================================================
    # MONTHLY RESERVE STATISTICS
    # =====================================================
    
    monthly_reserve = (
        monthly_gap
        .groupby(
            ["Month", "MonthSort"]
        )
        .apply(
            lambda df: pd.Series(
                {
                    "TotalHours": len(df),
    
                    "AdequateHours":
                    (
                        df["ReserveMargin"]
                        >=
                        df["RequiredReserve"]
                    ).sum()
                }
            )
        )
        .reset_index()
        .sort_values(
            "MonthSort"
        )
    )
    
    # =====================================================
    # RESERVE ADEQUACY
    # =====================================================
    
    monthly_reserve["ReserveAdequacyPct"] = (
        monthly_reserve["AdequateHours"]
        /
        monthly_reserve["TotalHours"]
        * 100
    )
   
    # =====================================================
    # CHART
    # =====================================================
    
    fig_reserve = go.Figure()
    #chart
    fig_reserve = go.Figure()

    #main line
    fig_reserve.add_trace(
        go.Scatter(
            x=monthly_reserve["Month"],
            y=monthly_reserve[
                "ReserveAdequacyPct"
            ],
            mode="lines+markers+text",
            text=
                monthly_reserve[
                    "ReserveAdequacyPct"
                ]
                .round(1)
                .astype(str)
                + "%",
            textposition="top center",
            name="Reserve Adequacy"
        )
    )

    #thresholds
    fig_reserve.add_hline(
        y=95,
        line_dash="dash",
        line_color="green",
        annotation_text="Excellent (95%)"
    )
    
    fig_reserve.add_hline(
        y=90,
        line_dash="dot",
        line_color="gold",
        annotation_text="Good (90%)"
    )
    
    fig_reserve.add_hline(
        y=80,
        line_dash="dot",
        line_color="orange",
        annotation_text="Fair (80%)"
    )

    #layouts
    fig_reserve.update_layout(
        title="Monthly Reserve Adequacy Trend",
        yaxis_title="Reserve Adequacy (%)",
        xaxis_title="Month",
        yaxis_range=[0, 105],
        height=400
    )
    
    st.plotly_chart(
        fig_reserve,
        use_container_width=True
    )

    st.caption(
        """
        Reserve Adequacy Legend:
    
        ≥95% = Excellent | 90-94.9% = Good |
        80-89.9% = Fair | <80% = Poor
        """
    )
    
    st.caption(
        """
        Reserve Adequacy (%) =
        (Hours Meeting Reserve Requirement ÷ Total Hours) × 100
        """
    )

    # =====================================================
    # MONTHLY RELIABILITY DETAILS TABLE
    # =====================================================
    monthly_detail = (
        monthly_gap
        .groupby(
            ["Month", "MonthSort"]
        )
        .apply(
            lambda df: pd.Series(
                {
                    "PeakDemand":
                        df["TotalDemand"].max(),
    
                    "AverageDemand":
                        df["TotalDemand"].mean(),
    
                    "MaxShortage":
                        df["ShortageMW"].max(),
    
                    "HoursWithShortage":
                        (
                            df["ShortageMW"] > 0
                        ).sum(),
    
                    "LowReserveHours":
                        (
                            df["ReserveMargin"]
                            <
                            df["RequiredReserve"]
                        ).sum(),
    
                    # Compliance checked HOURLY
                    "ReserveAdequacyPct":
                        (
                            (
                                df["ReserveMargin"]
                                >=
                                df["RequiredReserve"]
                            ).sum()
                            /
                            len(df)
                            * 100
                        ),
    
                    # Audit values only (not used for compliance)
                    "AveRegulatingReserveMW":
                        df["RegulatingReserve"].mean(),
    
                    "AveContingencyReserveMW":
                        df["ContingencyReserve"].mean(),
    
                    "AveRequiredReserveMW":
                        df["RequiredReserve"].mean(),
    
                    "AveReserveMarginMW":
                        df["ReserveMargin"].mean(),
    
                    "UnservedEnergy":
                        df["ShortageMW"].sum()
                }
            )
        )
        .reset_index()
        .sort_values(
            "MonthSort"
        )
    )

    #load factor
    monthly_detail["LoadFactor"] = (
        monthly_detail["AverageDemand"]
        /
        monthly_detail["PeakDemand"]
        * 100
    )

    monthly_detail["ReliabilityScore"] = (
        100
        -
        (
            monthly_detail["HoursWithShortage"]
            * 0.25
        )
        -
        (
            monthly_detail["LowReserveHours"]
            * 0.05
        )
    )
    
    monthly_detail["ReliabilityScore"] = (
        monthly_detail["ReliabilityScore"]
        .clip(
            lower=0,
            upper=100
        )
    )

    with st.expander(
        "Monthly Reliability Details",
        expanded=False
    ):
    
        st.dataframe(
            monthly_detail[
                [
                    "Month",
                    "PeakDemand",
                    "AverageDemand",
                    "MaxShortage",
                    "HoursWithShortage",
                    "LowReserveHours",
                    "ReserveAdequacyPct",
                    "AveRegulatingReserveMW",
                    "AveContingencyReserveMW",
                    "AveRequiredReserveMW",
                    "AveReserveMarginMW",
                    "UnservedEnergy",
                    "LoadFactor",
                    "ReliabilityScore"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )
    
        st.caption(
            """
            Regulating Reserve (MW)
            = Average Demand × 2.8%
    
            Contingency Reserve (MW)
            = Average Synchronized Generation × 10%
    
            Required Reserve (MW)
            = Regulating Reserve + Contingency Reserve
    
            Reserve Adequacy (%)
            = (Hours Meeting Required Reserve ÷ Total Hours) × 100
    
            Compliance is evaluated hourly using:
    
            Reserve Margin ≥ Required Reserve
            """
        )
