import pandas as pd
import streamlit as st


@st.cache_data
def read_excel_file(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".xlsb"):

        return pd.read_excel(
            uploaded_file,
            sheet_name=None,
            engine="pyxlsb"
        )

    return pd.read_excel(
        uploaded_file,
        sheet_name=None,
        engine="openpyxl"
    )


def load_data(config):

    # ==================================
    # MINDORO
    # ==================================

    if config["SYSTEM_NAME"] == "Mindoro":

        uploaded_file = st.sidebar.file_uploader(
            "Upload Mindoro Dispatch Summary",
            type=["xlsx", "xlsb"]
        )

        if uploaded_file is None:

            st.warning(
                "Please upload the Mindoro Dispatch Summary file."
            )

            st.stop()

        sheets = read_excel_file(
            uploaded_file
        )

        tables = []

        for sheet_name, sheet_df in sheets.items():

            sheet_df["SourceWorkbook"] = (
                uploaded_file.name
            )

            sheet_df["SourceSheet"] = (
                sheet_name
            )

            tables.append(
                sheet_df
            )

        return pd.concat(
            tables,
            ignore_index=True
        )

    # ==================================
    # PALAWAN / CATANDUANES
    # ==================================

    df = pd.read_excel(
        config["FILE_PATH"],
        sheet_name=config["SHEET_NAME"],
        engine="openpyxl"
    )

    return df
