import streamlit as st

from config.palawan import CONFIG as PALAWAN
from config.mindoro import CONFIG as MINDORO
from config.catanduanes import CONFIG as CATANDUANES

from core.load_data import load_data
from core.data_prep import prepare_data
from core.sidebar_filters import get_filters
from core.filter_data import filter_data
from core.demand_generation import build_demand_generation

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

    df = prepare_data(
        df,
        config
    )
    
    filters = get_filters(df)
    
    filtered = filter_data(
        df,
        filters
    )
    
    (
        total_demand,
        generation,
        total_generation,
        transfer_flow
    ) = build_demand_generation(
        filtered,
        config
    )
    
    st.success(
        f"{config['SYSTEM_NAME']} data loaded successfully."
    )
    
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
except Exception as e:

    st.exception(e)

    st.stop()
