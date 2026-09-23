import pandas as pd
import streamlit as st

@st.cache_data
def prepare_data(df, config):

    df = df.copy()

    datetime_column = config["DATETIME_COLUMN"]
    value_column = config["VALUE_COLUMN"]

    df["Datetime"] = pd.to_datetime(
        df[datetime_column],
        errors="coerce"
    )

    scale = config.get(
        "UNIT_SCALE",
        1
    )

    df["Value"] = (
        pd.to_numeric(
            df[value_column],
            errors="coerce"
        )
        / scale
    )

    attribute_filter = config.get(
        "ATTRIBUTE_FILTER"
    )
    
    if (
        attribute_filter
        and
        "Attribute" in df.columns
    ):
    
        df = df[
            df["Attribute"]
            .astype(str)
            .str.upper()
            ==
            attribute_filter.upper()
        ].copy()
    
    df["Month"] = df["Datetime"].dt.month

    df["Day"] = df["Datetime"].dt.day

    return df
