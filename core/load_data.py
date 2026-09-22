import pandas as pd
import streamlit as st
from pathlib import Path

def load_data(config):

    file_path = config["FILE_PATH"]

    st.write("File exists:", Path(file_path).exists())

    with open(file_path, "rb") as f:
        first_bytes = f.read(200)

    st.write("First bytes of file:")
    st.code(first_bytes)

    df = pd.read_excel(
        file_path,
        sheet_name=config["SHEET_NAME"],
        engine="openpyxl"
    )

    return df
