import streamlit as st

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
# TITLE
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
    # DATA PREP
    # =================================================

    df = prepare_data(
        df,
        config
    )

    capacity_reference = (
        build_capacity_reference(
            df
        )
    )

    capacity_reference = capacity_reference.rename(
        columns={
            "Dependable Capacity": "DependableMW"
        }
    )
    
    st.write(capacity_reference.columns.tolist())
    st.dataframe(capacity_reference.head())
    
    st.subheader(
        "Capacity Reference Validation"
    )
    
    st.dataframe(
        capacity_reference,
        use_container_width=True
    )
    
    # =================================================
    # FILTERS
    # =================================================

    filters = get_filters(df)

    filtered = filter_data(
        df,
        filters
    )

    # =================================================
    # DEMAND / GENERATION
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

    asset_performance = (
        build_asset_performance(
            generation,
            capacity_reference
        )
    )

    unit_capability = (
        build_unit_capability(
            generation,
            capacity_reference
        )
    )
   
    unit_capability_chart = (
        build_unit_capability_chart(
            unit_capability
        )
    )
    
    asset_performance_chart = (
        build_asset_performance_chart(
            asset_performance
        )
    )

    
    peak_support_chart = (
        build_peak_support_chart(
            peak_support
        )
    )

    st.plotly_chart(
        peak_support_chart,
        use_container_width=True
    )
    
    # =================================================
    # RELIABILITY
    # =================================================

    reliability = build_reliability(
        total_demand,
        total_generation,
        transfer_flow
    )

    capacity_planning = (
            build_capacity_planning(
                reliability,
                capacity_reference
            )
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
    
    st.success(
        f"{config['SYSTEM_NAME']} data loaded successfully."
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
    
    # =================================================
    # KPI VALIDATION
    # =================================================
    
    kpis = build_kpis(
        total_demand,
        total_generation,
        reliability
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

    # =================================================
    # LDC VALIDATION
    # =================================================
        
    ldc = build_ldc(
        total_demand
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
    
    st.subheader(
        "LDC Validation"
    )
    
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
    
    st.plotly_chart(
        unit_capability_chart,
        use_container_width=True
    )

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
            capacity_planning[
                "projection_df"
            ],
            use_container_width=True,
            hide_index=True
        )
    
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

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "OK",
            (
                asset_performance[
                    "RiskFlag"
                ]
                == "OK"
            ).sum()
        )
    
    with col2:
        st.metric(
            "Monitor",
            (
                asset_performance[
                    "RiskFlag"
                ]
                == "Monitor"
            ).sum()
        )
    
    with col3:
        st.metric(
            "Underperforming",
            (
                asset_performance[
                    "RiskFlag"
                ]
                == "Underperforming"
            ).sum()
        )
    
    st.plotly_chart(
        asset_performance_chart,
        use_container_width=True
    )
                
    # =================================================
    # KPI PREVIEW`
    # =================================================

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
    # VALIDATION TABLES
    # =================================================

    st.subheader("Total Demand")

    st.dataframe(
        total_demand.head(),
        use_container_width=True
    )

    st.subheader("Generation")

    st.dataframe(
        generation.head(),
        use_container_width=True
    )

    st.subheader("Total Generation")

    st.dataframe(
        total_generation.head(),
        use_container_width=True
    )

    st.subheader("Import Support")

    st.dataframe(
        transfer_flow.head(),
        use_container_width=True
    )

    st.subheader("Gap Data")

    st.dataframe(
        reliability["gap_df"].head(),
        use_container_width=True
    )

except Exception as e:

    st.exception(e)

    st.stop()
