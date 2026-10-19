import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config.palawan import CONFIG as PALAWAN
from config.mindoro import CONFIG as MINDORO
from config.catanduanes import CONFIG as CATANDUANES

from core.load_data import load_data
from core.data_prep import prepare_data
from core.sidebar_filters import get_filters
from core.filter_data import filter_data
from core.demand_generation import build_demand_generation
from core.reliability import build_reliability
from core.kpis import build_kpis
from core.reserve import build_reserve_assessment
from core.ldc import build_ldc
from core.ldc_segments import (
    build_ldc_segments,
    build_segment_table
)
from core.ldc_chart import build_ldc_chart
from core.reserve_dashboard import (
    build_reserve_dashboard
)
from core.reserve_trend import (
    build_reserve_trend
)
from core.operating_condition import (
    build_operating_condition_breakdown
)
from core.reserve_deficiency import (
    build_reserve_deficiency_table
)
from core.peak_hour import (
    build_peak_hour_analysis
)
from core.peak_hour_share import (
    build_peak_hour_share_chart
)
from core.capacity_reference import (
    build_capacity_reference
)
from core.peak_support_data import (
    build_peak_support_analysis
)
from core.peak_support_chart import (
    build_peak_support_chart
)
from core.asset_performance import (
    build_asset_performance
)
from core.asset_performance_chart import (
    build_asset_performance_chart
)
from core.unit_capability import (
    build_unit_capability
)
from core.unit_capability_chart import (
    build_unit_capability_chart
)
from core.capacity_planning import (
    build_capacity_planning
)

from core.reliability_monitor import (
    build_reliability_monitor
)
from core.plant_role_matrix import (
    build_plant_role_matrix
)
from core.demand_distribution import (
    build_demand_distribution
)

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Off-Grid Dispatch Dashboard",
    layout="wide"
)

# =====================================================
# DASHBOARD SELECTION
# =====================================================

dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Palawan",
        "Mindoro",
        "Catanduanes"
    ]
)

# =====================================================
# LOAD CONFIG
# =====================================================

if dashboard == "Palawan":
    config = PALAWAN

elif dashboard == "Mindoro":
    config = MINDORO

else:
    config = CATANDUANES

# =====================================================
# PAGE TITLE
# =====================================================

st.title(
    f"{config['SYSTEM_NAME']} Dispatch Dashboard"
)

# =====================================================
# REFRESH
# =====================================================

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# =====================================================
# LOAD DATA
# =====================================================

try:

    df = load_data(config)

    st.sidebar.success(
        f"Loaded {len(df):,} records"
    )

    # =================================================
    # DATA PREPARATION
    # =================================================

    df = prepare_data(
        df,
        config
    )

    capacity_reference = (
        build_capacity_reference(
            df,
            config
        )
    )
         
    # =================================================
    # DASHBOARD FILTERS
    # =================================================

    filters = get_filters(df)

    filtered = filter_data(
        df,
        filters
    )

    # =================================================
    # DEMAND / GENERATION MODEL
    # =================================================

    (
        total_demand,
        generation,
        total_generation,
        transfer_flow
    ) = build_demand_generation(
        filtered,
        config
    )

    # =====================================================
    # PEAK HOUR ANALYTICS
    # =====================================================
    
    peak_hour = (
        build_peak_hour_analysis(
            total_demand,
            generation
        )
    )
      
    peak_hour_share_fig = (
        build_peak_hour_share_chart(
            peak_hour[
                "peak_snapshot"
            ]
        )
    )

    peak_support = (
        build_peak_support_analysis(
            peak_hour,
            capacity_reference
        )
    )

    peak_support_chart = (
            build_peak_support_chart(
                peak_support
            )
        )
        
    # =====================================================
    # ASSET AND CAPABILITY ANALYTICS
    # =====================================================
    
    asset_performance = (
        build_asset_performance(
            generation,
            capacity_reference
        )
    )

    plant_role_matrix = (
        build_plant_role_matrix(
            asset_performance,
            peak_hour["peak_snapshot"]
        )
    )
    
    unit_capability = (
        build_unit_capability(
            generation,
            capacity_reference
        )
    )

    asset_performance_chart = (
            build_asset_performance_chart(
                asset_performance
            )
        )
    
    unit_capability_chart = (
        build_unit_capability_chart(
            unit_capability
        )
    )

    # =================================================
    # RELIABILITY ANALYTICS
    # =================================================
    
    reliability = build_reliability(
        total_demand,
        total_generation,
        transfer_flow
    )
    
    reserve = build_reserve_assessment(
        reliability
    )
    
    reserve_dashboard = (
        build_reserve_dashboard(
            reserve,
            reliability
        )
    )
    
    reserve_trend = (
        build_reserve_trend(
            reliability
        )
    )
    
    operating_condition = (
        build_operating_condition_breakdown(
            reliability
        )
    )
    
    reserve_deficiency_table = (
        build_reserve_deficiency_table(
            reliability
        )
    )

    # =====================================================
    # CAPACITY PLANNING
    # =====================================================

    capacity_planning = (
            build_capacity_planning(
                reliability,
                capacity_reference
            )
        )

    # =================================================
    # KPI VALIDATION
    # =================================================
    
    kpis = build_kpis(
        total_demand,
        total_generation,
        reliability
    )
#$$$$$$$$$$$$$$$$$$$
    # =====================================================
    # PALAWAN MIGRATION
    # KPI SUMMARY
    # =====================================================
    
    peak_row = reliability["gap_df"].loc[
        reliability["gap_df"]["TotalDemand"].idxmax()
    ]
    
    peak_datetime = peak_row["Datetime"]
    
    r1c1, r1c2, r1c3, r1c4, r1c5 = st.columns(5)
    
    with r1c1:
        st.metric(
            "Peak Demand",
            f"{reliability['peak_demand']:,.2f} MW"
        )
    
    with r1c2:
        st.metric(
            "Demand Energy",
            f"{kpis['demand_energy_mwh']:,.2f} MWh"
        )
    
    with r1c3:
        st.metric(
            "Generated Energy",
            f"{kpis['generated_energy_mwh']:,.2f} MWh"
        )
    
    with r1c4:
        st.metric(
            "Unserved Energy",
            f"{reliability['unserved_energy']:,.2f} MWh"
        )
    
    with r1c5:
        st.metric(
            "Energy Served",
            f"{kpis['energy_served_pct']:.2f}%"
        )
    
    r2c1, r2c2, r2c3, r2c4 = st.columns(4)
    
    with r2c1:
        st.metric(
            "Hours with Shortage",
            f"{reliability['hours_with_shortage']:,}"
        )
    
    with r2c2:
        st.metric(
            "Low Reserve Hours",
            f"{reliability['hours_low_reserve']:,}"
        )
    
    with r2c3:
        st.metric(
            "Load Factor",
            f"{kpis['load_factor']:.1f}%"
        )
    
    with r2c4:
        st.metric(
            "Peak Demand Time",
            peak_datetime.strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    show_breakdown = st.toggle(
        "Break down by power plant",
        value=False
    )

    with st.sidebar.expander(
        "Technology Mapping",
        expanded=False
    ):
    
        plant_mapping = pd.DataFrame(
            {
                "Plant": sorted(
                    generation["Plant"]
                    .dropna()
                    .unique()
                )
            }
        )
    
        plant_mapping["Technology"] = (
            plant_mapping["Plant"]
            .map(
                config.get(
                    "TECHNOLOGY_MAPPING",
                    {}
                )
            )
            .fillna("Other")
        )
    
        plant_mapping = st.data_editor(
            plant_mapping,
            column_config={
                "Technology":
                st.column_config.SelectboxColumn(
                    "Technology",
                    options=[
                        "Bunker",
                        "Diesel",
                        "Thermal",
                        "Solar",
                        "Hydro",
                        "Wind",
                        "Biomass",
                        "Other"
                    ]
                )
            },
            hide_index=True,
            use_container_width=True
        )
    
        technology_map = dict(
            zip(
                plant_mapping["Plant"],
                plant_mapping["Technology"]
            )
        )

        st.caption(
            "Copy this dictionary into TECHNOLOGY_MAPPING in config."
        )
    
        st.code(
            repr(technology_map),
            language="python"
        )
    
    generation_mix = generation.copy()
    
    generation_mix["Technology"] = (
        generation_mix["Plant"]
        .map(technology_map)
        .fillna("Other")
    )
    
    tech_colors = {
        "Diesel": "#1565C0",
        "Thermal": "#E53935",
        "Bunker": "#FB8C00",
        "Solar": "#FDD835",
        "Hydro": "#00ACC1",
        "Wind": "#26A69A",
        "Biomass": "#7CB342",
        "Other": "#757575"
    }
    
    # =====================================================
    # TECHNOLOGY ORDER
    # =====================================================
    
    technology_order = (
        generation_mix
        .groupby(
            "Technology"
        )["Value"]
        .sum()
        .sort_values(
            ascending=False
        )
        .index
        .tolist()
    )
    
    # =====================================================
    # TOGGLE LOGIC
    # =====================================================
    
    if show_breakdown:
    
        tech_mix = (
            generation_mix
            .groupby(
                ["Technology", "Plant"],
                as_index=False
            )["Value"]
            .sum()
        )
    
        tech_mix["Share"] = (
            tech_mix["Value"]
            /
            tech_mix["Value"].sum()
            * 100
        )
    
        tech_mix["Technology"] = pd.Categorical(
            tech_mix["Technology"],
            categories=technology_order,
            ordered=True
        )
    
        tech_mix = tech_mix.sort_values(
            ["Technology", "Share"],
            ascending=[True, False]
        )
    
        tech_mix.rename(
            columns={
                "Plant": "Display"
            },
            inplace=True
        )
    
    else:
    
        tech_mix = (
            generation_mix
            .groupby(
                "Technology",
                as_index=False
            )["Value"]
            .sum()
        )
    
        tech_mix["Share"] = (
            tech_mix["Value"]
            /
            tech_mix["Value"].sum()
            * 100
        )
    
        tech_mix["Technology"] = pd.Categorical(
            tech_mix["Technology"],
            categories=technology_order,
            ordered=True
        )
    
        tech_mix = tech_mix.sort_values(
            "Technology"
        )
    
        tech_mix.rename(
            columns={
                "Technology": "Display"
            },
            inplace=True
        )
    
    fig_tech = go.Figure()
    
    for _, row in tech_mix.iterrows():
    
        fig_tech.add_trace(
            go.Bar(
                y=[""],
                x=[row["Share"]],
                name=row["Display"],
                orientation="h",
            marker_color=(
                tech_colors.get(
                    technology_map.get(
                        row["Display"],
                        "Other"
                    ),
                    "#757575"
                )
                if show_breakdown
                else
                tech_colors.get(
                    row["Display"],
                    "#757575"
                )
            ),
                text=(
                    f"{row['Display']}<br>"
                    f"{row['Share']:.1f}%"
                ),
                textposition="inside"
            )
        )

    fig_tech.update_layout(
        barmode="stack",
        height=220,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=40
        ),
        xaxis_title=
            "Share of Generated Energy (%)",
        showlegend=False
    )
    
    st.plotly_chart(
        fig_tech,
        use_container_width=True
    )

    # =====================================================
    # MONTHLY GENERATION SHARE BY TECHNOLOGY
    # =====================================================
    
    st.subheader(
        "Monthly Generation Share by Technology"
    )
    
    monthly_tech = generation_mix.copy()
    
    monthly_tech["Month"] = (
        monthly_tech["Datetime"]
        .dt.strftime("%b %Y")
    )
    
    # Hidden chronological sort column
    monthly_tech["MonthSort"] = (
        monthly_tech["Datetime"]
        .dt.to_period("M")
    )
    
    monthly_tech = (
        monthly_tech
        .groupby(
            ["Month", "MonthSort", "Technology"],
            as_index=False
        )["Value"]
        .sum()
    )
    
    # =====================================================
    # COMPUTE MONTHLY SHARE
    # =====================================================
    
    monthly_total = (
        monthly_tech
        .groupby("Month")["Value"]
        .transform("sum")
    )
    
    monthly_tech["SharePct"] = (
        monthly_tech["Value"]
        /
        monthly_total
        * 100
    )
    
    # =====================================================
    # CREATE MATRIX
    # =====================================================
    
    tech_matrix = (
        monthly_tech
        .pivot(
            index="Technology",
            columns="Month",
            values="SharePct"
        )
        .fillna(0)
    )
    
    # =====================================================
    # ENSURE MONTHS ARE PROPERLY SORTED
    # =====================================================
    
    month_order = (
        monthly_tech[
            ["Month", "MonthSort"]
        ]
        .drop_duplicates()
        .sort_values(
            "MonthSort"
        )["Month"]
        .tolist()
    )
    
    tech_matrix = tech_matrix[
        month_order
    ]
    
    # =====================================================
    # CONSISTENT TECHNOLOGY ORDER
    # =====================================================
    
    technology_order = [
        tech
        for tech in tech_colors.keys()
        if tech in tech_matrix.index
    ]
    
    tech_matrix = tech_matrix.reindex(
        technology_order
    )
    
    # =====================================================
    # HEATMAP
    # =====================================================
    
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=tech_matrix.values,
            x=tech_matrix.columns,
            y=tech_matrix.index,
            text=
                tech_matrix.round(1)
                .astype(str)
                + "%",
            texttemplate="%{text}",
            colorscale="Blues",
            zmin=0,
            zmax=100,
            colorbar=dict(
                title="% Share"
            )
        )
    )
    
    # =====================================================
    # FORMAT LAYOUT OF HEATMAP
    # =====================================================
    
    fig_heatmap.update_layout(
        height=250,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        )
    )
    
    # =====================================================
    # DISPLAY HEATMAP
    # =====================================================
    
    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )
    
    # =====================================================
    # Matrix Table
    # =====================================================
    
    with st.expander(
        "View Monthly Technology Share Matrix (%)",
        expanded=False
    ):
    
        st.dataframe(
            tech_matrix.round(1),
            use_container_width=True
        )

    # =====================================================
    # Reliability Health Monitor
    # =====================================================

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

    # =====================================================
    # DEMAND DISTRIBUTION ANALYSIS
    # =====================================================
    
    st.subheader(
        "Demand Distribution Analysis"
    )
    
    b1, b2 = st.columns(2)
    
    with b1:
    
        st.plotly_chart(
            demand_distribution[
                "daily_peak_fig"
            ],
            use_container_width=True
        )
    
    with b2:
    
        st.plotly_chart(
            demand_distribution[
                "hourly_fig"
            ],
            use_container_width=True
        )
    
    st.metric(
        "Load Factor",
        f"{demand_distribution['load_factor']:.1f}%"
    )
    
    st.plotly_chart(
        demand_distribution[
            "heatmap_fig"
        ],
        use_container_width=True
    )
    
    with st.expander(
        "View Heatmap Source Data",
        expanded=False
    ):
    
        st.dataframe(
            demand_distribution[
                "heatmap_table"
            ].round(1),
            use_container_width=True
        )
    


    
#$$$$$$$$$$$$$$$$$$$
    reliability_monitor = (
        build_reliability_monitor(
            reliability,
            reserve,
            kpis
        )
    )
    
    st.subheader("KPI Validation")
    

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Demand Energy",
            f"{kpis['demand_energy_mwh']:,.2f}"
        )
    
    with col2:
        st.metric(
            "Generated Energy",
            f"{kpis['generated_energy_mwh']:,.2f}"
        )
    
    with col3:
        st.metric(
            "Energy Served %",
            f"{kpis['energy_served_pct']:,.2f}%"
        )
    
    with col4:
        st.metric(
            "Load Factor",
            f"{kpis['load_factor']:,.2f}%"
        )
   
    # =====================================================
    # RELIABILITY HEALTH MONITOR
    # =====================================================
    
    st.subheader(
        "Reliability Health Monitor"
    )
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            "Energy Served %",
            f"{reliability_monitor['energy_served_pct']:.2f}%"
        )
    
    with c2:
        st.metric(
            "Reserve Compliance %",
            f"{reliability_monitor['reserve_compliance_pct']:.2f}%"
        )
    
    with c3:
        st.metric(
            "Shortage Hours",
            reliability_monitor[
                "shortage_hours"
            ]
        )
    
    with c4:
        st.metric(
            "System Health",
            reliability_monitor[
                "overall_status"
            ]
        )  

    # =====================================================
    # RESERVE SECURITY ASSESSMENT
    # =====================================================
    
    st.subheader(
        "Reserve Security Assessment"
    )
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            "Hours Evaluated",
            reserve_dashboard[
                "total_hours"
            ]
        )
    
    with c2:
        st.metric(
            "Demand Served Hours",
            reserve_dashboard[
                "served_hours"
            ]
        )
    
    with c3:
        st.metric(
            "Unserved Hours",
            reserve_dashboard[
                "unserved_hours"
            ]
        )
    
    with c4:
        st.metric(
            "Worst Deficiency",
            f"{reserve_dashboard['worst_reserve_deficiency']:,.2f}"
        )

    st.subheader(
        "Reserve Validation"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Low Reserve Hours",
            reserve["hours_low_reserve"]
        )
    
    with col2:
        st.metric(
            "Reserve Compliance %",
            f"{reserve['reserve_compliance_pct']:.2f}%"
        )

    st.subheader(
        "Monthly Reserve Compliance Trend"
    )
    
    st.plotly_chart(
        reserve_trend["figure"],
        use_container_width=True
    )

    with st.expander(
        "Monthly Reserve Compliance Data",
        expanded=False
    ):
    
        st.dataframe(
            reserve_trend["monthly"],
            use_container_width=True
        )

    st.subheader(
        "Operating Condition Breakdown"
    )
    
    st.plotly_chart(
        operating_condition["figure"],
        use_container_width=True
    )

    with st.expander(
        "Operating Condition Data",
        expanded=False
    ):
    
        st.write(
            f"Adequate Reserve Hours: "
            f"{operating_condition['adequate_hours']:,}"
        )
    
        st.write(
            f"Reserve Deficient Hours: "
            f"{operating_condition['reserve_deficient_hours']:,}"
        )
    
        st.write(
            f"Unserved Demand Hours: "
            f"{operating_condition['shortage_hours']:,}"
        )
    
    with st.expander(
        "Reserve Deficient Hours",
        expanded=False
    ):
    
        st.dataframe(
            reserve_deficiency_table.round(
                {
                    "TotalDemand": 2,
                    "TotalSupply": 2,
                    "ReserveMargin": 2,
                    "RequiredReserve": 2,
                    "ReserveDeficiency": 2
                }
            ),
            use_container_width=True,
            hide_index=True
        )
    
        st.dataframe(
            reserve_deficiency_table.round(
                {
                    "TotalDemand": 2,
                    "TotalSupply": 2,
                    "ReserveMargin": 2,
                    "RequiredReserve": 2,
                    "ReserveDeficiency": 2
                }
            ),
            use_container_width=True,
            hide_index=True
        )
    
    # =================================================
    # LDC VALIDATION
    # =================================================
        
    ldc = build_ldc(
        total_demand
    )

    demand_distribution = (
        build_demand_distribution(
            total_demand
        )
    )
    
    ldc_segments = build_ldc_segments(
        ldc
    )

    segment_table = build_segment_table(
        ldc,
        ldc_segments["boundaries"],
        ldc_segments["compressed_points"]
    )

    ldc_fig, segment_summary = (
        build_ldc_chart(
            ldc,
            ldc_segments["boundaries"],
            ldc_segments["compressed_points"]
        )
    )

    # ============================================================================
    # ============================================================================
    # MIGRATION BOUNDARY
    #
    # ABOVE THIS LINE:
    #     Production dashboard content migrated from the approved
    #     working Palawan/Mindoro/Catanduanes dashboards.
    #
    # BELOW THIS LINE:
    #     Temporary validation, diagnostics, framework testing,
    #     migration-era QA outputs, comparison tables, and
    #     development checkpoints.
    #
    # DELETE EVERYTHING BELOW THIS SECTION ONCE MIGRATION IS COMPLETE.
    # ============================================================================
    # ============================================================================
    
    # =================================================
    # LDC SEGMENTATION VALIDATION
    # =================================================
    
    st.subheader(
        "LDC Segmentation Validation"
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Original Points",
            ldc_segments["original_points"]
        )
    
    with col2:
        st.metric(
            "Compressed Points",
            ldc_segments["compressed_points"]
        )
    
    with col3:
        st.metric(
            "Recommended Segments",
            ldc_segments["recommended_segments"]
        )
    
    with col4:
        st.metric(
            "Total SSE",
            f"{ldc_segments['total_sse']:,.0f}"
        )
    
    st.dataframe(
        ldc_segments["sse_df"],
        use_container_width=True
    )
    
    # =================================================
    # SEGMENT TABLE
    # =================================================
    
    st.subheader(
        "Segment Table Validation"
    )
    
    st.dataframe(
        segment_table,
        use_container_width=True
    )


    # =====================================================
    # LOAD DURATION CURVE
    # =====================================================
    
    st.subheader(
        "Load Duration Curve"
    )
    
    st.plotly_chart(
        ldc_fig,
        use_container_width=True
    )

    st.markdown(
        "##### Segment Summary"
    )
    
    st.dataframe(
        segment_summary,
        use_container_width=True,
        hide_index=True
    )

    with st.expander(
        "Advanced LDC Segmentation Analysis",
        expanded=False
    ):
    
        st.metric(
            "Current Segmentation SSE",
            f"{ldc_segments['total_sse']:,.0f}"
        )
    
        st.markdown(
            f"""
    ### Recommended Segmentation
    
    Recommended Segments:
    **{ldc_segments['recommended_segments']}**
    
    Current Selection:
    **{ldc_segments['recommended_segments']}**
    
    The elbow method indicates
    that additional segmentation
    beyond this point provides
    diminishing improvement.
    """
        )
    
        st.dataframe(
            segment_table,
            use_container_width=True
        )
    
    # =================================================
    # LDC VALIDATION
    # =================================================
    
    with st.expander(
        "LDC Validation",
        expanded=False
    ):
    
        col1, col2 = st.columns(2)
    
        with col1:
            st.metric(
                "Peak Load",
                f"{ldc['DemandMW'].max():,.2f}"
            )
    
        with col2:
            st.metric(
                "Minimum Load",
                f"{ldc['DemandMW'].min():,.2f}"
            )
    
        st.dataframe(
            ldc.head(20),
            use_container_width=True
        )

    # =====================================================
    # PEAK HOUR PERFORMANCE ANALYSIS
    # =====================================================
    
    st.subheader(
        "Peak Hour Performance Analysis"
    )
    
    snapshot = (
        peak_hour["peak_snapshot"]
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Peak Threshold",
            f"{peak_hour['peak_threshold']:,.2f}"
        )
    
    with col2:
        st.metric(
            "Peak Hours",
            len(
                peak_hour["peak_hours"]
            )
        )
    
    with col3:
        st.metric(
            "Plants Supporting Peak",
            len(snapshot)
        )
    
    with st.expander(
        "Peak Hour Snapshot",
        expanded=False
    ):
    
        st.dataframe(
            snapshot.round(2),
            use_container_width=True,
            hide_index=True
        )
    
    st.plotly_chart(
        peak_hour_share_fig,
        use_container_width=True
    )

    st.markdown(
        "##### Peak Hour Energy Contribution Share"
    )
    
    with st.expander(
        "Peak Hour Energy Share Data",
        expanded=False
    ):
    
        st.dataframe(
            peak_hour[
                "peak_snapshot"
            ][
                [
                    "Plant",
                    "AvgPeakMW",
                    "MaxPeakMW",
                    "PeakEnergyMWh",
                    "PeakEnergySharePct"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # PEAK SUPPORT PERFORMANCE
    # =====================================================
    
    st.subheader(
        "Peak Support Performance"
    )

    with st.expander(
        "Peak Support Table",
        expanded=False
    ):

        st.dataframe(
            peak_support[
                [
                    "Plant",
                    "AvgPeakMW",
                    "MaxPeakMW",
                    "DependableMW",
                    "PeakSupportPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ].round(2),
            use_container_width=True,
            hide_index=True
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "OK",
            (
                peak_support["RiskFlag"]
                == "OK"
            ).sum()
        )

    with col2:
        st.metric(
            "Monitor",
            (
                peak_support["RiskFlag"]
                == "Monitor"
            ).sum()
        )

    with col3:
        st.metric(
            "Underperforming",
            (
                peak_support["RiskFlag"]
                == "Underperforming"
            ).sum()
        )

    st.markdown(
        "##### Peak Support Achievement Chart"
    )
    
    st.plotly_chart(
        peak_support_chart,
        use_container_width=True
    )
 
        
    st.dataframe(
        peak_hour[
            "peak_snapshot"
        ][
            [
                "Plant",
                "AvgPeakMW",
                "MaxPeakMW",
                "PeakEnergyMWh",
                "PeakEnergySharePct"
            ]
        ].round(2),
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # PLANT ASSET PERFORMANCE ASSESSMENT
    # =====================================================
    
    st.subheader(
        "Plant Asset Performance Assessment"
    )
    
    with st.expander(
        "Asset Performance Table",
        expanded=False
    ):
    
        st.dataframe(
            asset_performance[
                [
                    "Plant",
                    "DependableMW",
                    "AvgMW",
                    "MaxObservedMW",
                    "UtilizationFactorPct",
                    "CapabilityRealizationPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ].round(2),
    
            use_container_width=True,
            hide_index=True
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "OK",
            (
                asset_performance["RiskFlag"]
                == "OK"
            ).sum()
        )
    
    with col2:
        st.metric(
            "Monitor",
            (
                asset_performance["RiskFlag"]
                == "Monitor"
            ).sum()
        )
    
    with col3:
        st.metric(
            "Underperforming",
            (
                asset_performance["RiskFlag"]
                == "Underperforming"
            ).sum()
        )
    
    st.markdown(
        "##### Capability Realization by Plant"
    )
    
    st.plotly_chart(
        asset_performance_chart,
        use_container_width=True
    )

    # =====================================================
    # UNIT CAPABILITY REALIZATION
    # =====================================================
    
    st.subheader(
        "Unit Capability Realization"
    )
    
    with st.expander(
        "Unit Capability Table",
        expanded=False
    ):
    
        st.dataframe(
            unit_capability[
                [
                    "Plant",
                    "DependableMW",
                    "AvgMW",
                    "MaxObservedMW",
                    "OperatingHours",
                    "HoursAbove80Pct",
                    "UtilizationFactorPct",
                    "CapabilityRealizationPct",
                    "SustainedCapabilityPct",
                    "RiskFlag",
                    "Remarks"
                ]
            ].round(2),
    
            use_container_width=True,
            hide_index=True
        )

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "OK",
            (
                unit_capability[
                    "RiskFlag"
                ]
                == "OK"
            ).sum()
        )
    
    with col2:
        st.metric(
            "Monitor",
            (
                unit_capability[
                    "RiskFlag"
                ]
                == "Monitor"
            ).sum()
        )
    
    with col3:
        st.metric(
            "Underperforming",
            (
                unit_capability[
                    "RiskFlag"
                ]
                == "Underperforming"
            ).sum()
        )
    
    st.markdown(
        "##### Unit Sustained Capability Assessment"
    )
    
    st.plotly_chart(
        unit_capability_chart,
        use_container_width=True
    )

    # =====================================================
    # CAPACITY OUTLOOK
    # =====================================================
    
    st.subheader(
        "Capacity Outlook"
    )
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric(
            "Current Peak Demand",
            f"{capacity_planning['peak_demand']:,.2f}"
        )
    
    with c2:
        st.metric(
            "Projected Peak Demand",
            f"{capacity_planning['projected_peak']:,.2f}"
        )
    
    with c3:
        st.metric(
            "Available Capacity",
            f"{capacity_planning['available_capacity']:,.2f}"
        )
    
    with c4:
        st.metric(
            "Additional Capacity Needed",
            f"{capacity_planning['required_capacity']:,.2f}"
        )
    
    with st.expander(
        "10-Year Capacity Planning Outlook",
        expanded=False
    ):
    
        st.dataframe(
            capacity_planning["projection_df"],
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # PLANT ROLE MATRIX
    # =====================================================
    
    st.subheader(
        "Plant Role Matrix"
    )
    
    with st.expander(
        "Plant Role Classification",
        expanded=False
    ):
    
        st.dataframe(
            plant_role_matrix[
                [
                    "Plant",
                    "EnergySharePct",
                    "PeakSharePct",
                    "Role"
                ]
            ].round(2),
    
            use_container_width=True,
            hide_index=True
        )

    role_counts = (
        plant_role_matrix["Role"]
        .value_counts()
        .reset_index()
    )
    
    role_counts.columns = [
        "Role",
        "Count"
    ]
    
    st.dataframe(
        role_counts,
        use_container_width=True,
        hide_index=True
    )
                  
    # =====================================================
    # RELIABILITY SUMMARY
    # =====================================================

    st.subheader("Reliability Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Peak Demand",
            f"{reliability['peak_demand']:,.2f}"
        )
    
    with col2:
        st.metric(
            "Hours With Shortage",
            reliability["hours_with_shortage"]
        )
    
    with col3:
        st.metric(
            "Low Reserve Hours",
            reliability["hours_low_reserve"]
        )
    
    with col4:
        st.metric(
            "Unserved Energy",
            f"{reliability['unserved_energy']:,.2f}"
        )
    
    with col5:
        st.metric(
            "Peak Demand Time",
            str(reliability["peak_datetime"])
        )

    # =================================================
    # TECHNICAL VALIDATION TABLES
    # =================================================

    with st.expander(
        "Technical Validation Tables",
        expanded=False
    ):

        st.markdown("### Total Demand")

        st.dataframe(
            total_demand.head(),
            use_container_width=True
        )

        st.markdown("### Generation")

        st.dataframe(
            generation.head(),
            use_container_width=True
        )

        st.markdown("### Total Generation")

        st.dataframe(
            total_generation.head(),
            use_container_width=True
        )

        st.markdown("### Import Support")

        st.dataframe(
            transfer_flow.head(),
            use_container_width=True
        )

        st.markdown("### Gap Data")

        st.dataframe(
            reliability["gap_df"].head(),
            use_container_width=True
        )

# =====================================================
# ERROR HANDLING
# =====================================================

except Exception as e:

    st.exception(e)

    st.stop()

# ============================================================================
# END OF TEMPORARY VALIDATION SECTION
# ============================================================================
