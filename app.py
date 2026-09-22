import streamlit as st

from config.palawan import CONFIG as PALAWAN
from config.mindoro import CONFIG as MINDORO
from config.catanduanes import CONFIG as CATANDUANES

dashboard = st.sidebar.selectbox(
    "Select Dashboard",
    ["Palawan", "Mindoro", "Catanduanes"]
)

if dashboard == "Palawan":
    config = PALAWAN

elif dashboard == "Mindoro":
    config = MINDORO

else:
    config = CATANDUANES

st.title(config["SYSTEM_NAME"])
