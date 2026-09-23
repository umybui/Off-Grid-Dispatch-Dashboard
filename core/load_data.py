import pandas as pd
import streamlit as st

@st.cache_data
def load_data(config):

    df = pd.read_excel(
        config["FILE_PATH"],
        sheet_name=config["SHEET_NAME"],
        engine="openpyxl"
    )

    return df
