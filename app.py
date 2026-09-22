import streamlit as st

from config.palawan import CONFIG as PALAWAN
from config.mindoro import CONFIG as MINDORO
from config.catanduanes import CONFIG as CATANDUANES

from core.load_data import load_data

# -----------------------------
# Dashboard Selection
# -----------------------------
dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    ["Palawan", "Mindoro", "Catanduanes"]
)

# -----------------------------
# Load Config
# -----------------------------
if dashboard == "Palawan":
    config = PALAWAN

elif dashboard == "Mindoro":
    config = MINDORO

else:
    config = CATANDUANES

# -----------------------------
# Page Title
# -----------------------------

st.write("CONFIG CONTENTS:")
st.write(config)

# =====================================================
# LOAD DATA
# =====================================================

try:

    st.write("Looking for file:")
    st.write(config["FILE_PATH"])

    st.write("Using worksheet:")
    st.write(config["SHEET_NAME"])

    df = load_data(config)

    st.success(
        f"Loaded {config['SYSTEM_NAME']} data successfully."
    )

    st.write("Rows:", len(df))
    st.write("Columns:", len(df.columns))

    st.dataframe(df.head())

except Exception as e:

    st.exception(e)
