import pandas as pd
import streamlit as st

st.warning("USING CAPACITY_REFERENCE.PY VERSION 2026-09-26")

def build_capacity_reference(
    df
):

    if "Attribute" not in df.columns:
        return pd.DataFrame()

    capacity_data = (
        df[
            df["Attribute"]
            .astype(str)
            .str.upper()
            .isin(
                [
                    "INSTALLED CAPACITY (MW)",
                    "DEPENDABLE CAPACITY"
                ]
            )
        ]
        .copy()
    )

    if len(capacity_data) == 0:
        return pd.DataFrame()

    available_capacity_tbl = (
        capacity_data
        .pivot_table(
            index=["Plant"],
            columns="Attribute",
            values="Value",
            aggfunc="max"
        )
        .reset_index()
    )

    available_capacity_tbl.rename(
        columns={
            "DEPENDABLE CAPACITY":
                "DependableMW",

            "INSTALLED CAPACITY (MW)":
                "InstalledMW"
        },
        inplace=True
    )

    if "DependableMW" in available_capacity_tbl.columns:

        available_capacity_tbl[
            "AvailableMW"
        ] = (
            available_capacity_tbl[
                "DependableMW"
            ]
        )

    return available_capacity_tbl
