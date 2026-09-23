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
  
    # =================================================
    # RELIABILITY
    # =================================================

    reliability = build_reliability(
        total_demand,
        total_generation,
        transfer_flow
    )

    st.success(
        f"{config['SYSTEM_NAME']} data loaded successfully."
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
