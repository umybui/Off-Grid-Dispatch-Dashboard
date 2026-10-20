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
from core.plant_role_matrix import (
    build_plant_role_matrix
)
from core.demand_distribution import (
    build_demand_distribution
)
from core.executive_summary import (
    build_executive_summary
)
from core.generation_mix_dashboard import (
    build_generation_mix_dashboard
)
from core.reliability_monitor import (
    build_reliability_monitor
)
from core.demand_distribution_dashboard import (
    build_demand_distribution_dashboard
)
from core.ldc_dashboard import (
    build_ldc_dashboard
)
from core.reserve_security_dashboard import (
    build_reserve_security_dashboard
)
from core.reserve_trend_dashboard import (
    build_reserve_trend_dashboard
)
from core.reserve_deficiency_dashboard import (
    build_reserve_deficiency_dashboard
)
from core.capacity_planning_dashboard import (
    build_capacity_planning_dashboard
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

    # =====================================================
    # DEMAND DISTRIBUTION
    # =====================================================
    
    demand_distribution = (
        build_demand_distribution(
            total_demand
        )
    )
           
#$$$$$$$$$$$$$$$$$$$
    # =====================================================
    # PALAWAN MIGRATION
    # KPI SUMMARY
    # =====================================================

    build_executive_summary(
        reliability,
        kpis
    )

    build_generation_mix_dashboard(
        generation,
        config
    )

    build_reliability_monitor(
        reliability,
        kpis
    )

    build_demand_distribution_dashboard(
        demand_distribution
    )
   
    build_ldc_dashboard(
    total_demand
    )

    build_reserve_security_dashboard(
        reserve,
        reserve_dashboard
    )
    
    build_reserve_trend_dashboard(
        reserve_trend
    )
    
    build_reserve_deficiency_dashboard(
        operating_condition,
        reserve_deficiency_table
    )
    
    build_capacity_planning_dashboard(
        capacity_planning
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
