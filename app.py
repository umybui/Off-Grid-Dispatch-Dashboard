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
from core.shortage_events import (
    build_shortage_events
)
from core.shortage_event_dashboard import (
    build_shortage_event_dashboard
)
from core.plant_contribution import (
    build_plant_contribution
)
from core.plant_contribution_dashboard import (
    build_plant_contribution_dashboard
)
from core.plant_role_dashboard import (
    build_plant_role_dashboard
)
from core.peak_hour_dashboard import (
    build_peak_hour_dashboard
)
from core.capacity_outlook_dashboard import (
    build_capacity_outlook_dashboard
)
from core.historical_dispatch_dashboard import (
    build_historical_dispatch_dashboard
)
from core.peak_support_dashboard import (
    build_peak_support_dashboard
)
from core.daily_peak_mix import (
    build_daily_peak_mix
)
from core.daily_peak_mix_dashboard import (
    build_daily_peak_mix_dashboard
)
from core.dependable_audit import (
    build_dependable_audit
)
from core.dependable_audit_dashboard import (
    build_dependable_audit_dashboard
)
from core.asset_performance_dashboard import (
    build_asset_performance_dashboard
)
from core.unit_capability_dashboard import (
    build_unit_capability_dashboard
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
 
    dependable_audit = (
        build_dependable_audit(
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
            generation_unit
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

    plant_contribution = (
        build_plant_contribution(
            generation
        )
    )

    daily_peak_mix = (
        build_daily_peak_mix(
            total_demand,
            generation,
            capacity_reference
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

    shortage_events = (
        build_shortage_events(
            reliability
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
        kpis,
        capacity_planning
    )

    st.divider()
    
    build_generation_mix_dashboard(
        generation,
        config
    )

    st.divider()
 
    build_reliability_monitor(
        reliability,
        kpis
    )

    st.divider()
 
    build_demand_distribution_dashboard(
        demand_distribution
    )
   
    st.divider()
 
    build_ldc_dashboard(
    total_demand
    )

    st.divider()
 
    build_reserve_security_dashboard(
        reserve,
        reserve_dashboard,
        reliability
    )

    st.divider()
 
    build_reserve_deficiency_dashboard(
        operating_condition,
        reserve_deficiency_table
    )

    st.divider()
 
    build_reserve_trend_dashboard(
        reserve_trend
    )   

    st.divider()
 
    build_shortage_event_dashboard(
        shortage_events
    )

    st.divider()
  
    build_plant_contribution_dashboard(
        plant_contribution
    )

    st.divider()

    build_plant_role_dashboard(
        plant_role_matrix
    )

    st.divider()

    st.write(
        peak_hour["peak_snapshot"]
        .columns
    )
    
    st.dataframe(
        peak_hour["peak_snapshot"]
        .head(20)
    )

    build_peak_hour_dashboard(
        peak_hour,
        peak_hour_share_fig
    )

    st.divider()
    
    build_capacity_outlook_dashboard(
        capacity_planning,
        capacity_reference
    )

    st.divider()

    build_historical_dispatch_dashboard(
        generation,
        total_demand,
        total_generation
    )

    st.divider()

    build_daily_peak_mix_dashboard(
        daily_peak_mix
    )

    st.divider()

    build_dependable_audit_dashboard(
        dependable_audit
    )
    
    st.divider()
    
    build_asset_performance_dashboard(
        asset_performance,
        asset_performance_chart
    )   

    st.divider()
    
    build_unit_capability_dashboard(
        unit_capability,
        unit_capability_chart
    )
    
#$$$$$$$$$$$$$$$$$$$

except Exception as e:

    st.exception(e)

    st.stop()
