import pandas as pd
import streamlit as st

def build_capacity_reference(
    df,
    config=None
):

    if (
        config is not None
        and
        "DEPENDABLE_REFERENCE" in config
    ):
    
        capacity_reference = pd.DataFrame(
            config["DEPENDABLE_REFERENCE"]
        )
    
        capacity_reference["InstalledMW"] = (
            capacity_reference["DependableMW"]
        )
    
        capacity_reference["AvailableMW"] = (
            capacity_reference["DependableMW"]
        )
    
        return capacity_reference
    
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
                        "DEPENDABLE CAPACITY",
                
                        "INSTALLED CAPACITY (KW)",
                        "GUARANTEED DEPENDABLE CAPACITY (KW)",
                        "AVAILABLE CAPACITY (KW)"
                    ]
                )
            ]
            .copy()
        )

    

    if len(capacity_data) == 0:
        return pd.DataFrame()

    agg_func = (
        config.get(
            "CAPACITY_AGGREGATION",
            "sum"
        )
        if config
        else "sum"
    )
    
    available_capacity_tbl = (
        capacity_data
        .pivot_table(
            index=["Plant"],
            columns="Attribute",
            values="Value",
            aggfunc=agg_func
        )
        .reset_index()
    )

    available_capacity_tbl.columns = [
        str(col).strip()
        for col in available_capacity_tbl.columns
    ]
    
    available_capacity_tbl.rename(
        columns={
    
            "Dependable Capacity":
                "DependableMW",
    
            "Guaranteed Dependable Capacity (kW)":
                "DependableMW",
    
            "Installed Capacity (kW)":
                "InstalledMW",
    
            "Installed Capacity (MW)":
                "InstalledMW",
    
            "Available Capacity (kW)":
                "AvailableMW"
    
        },
        inplace=True
    )

    if (
        "AvailableMW"
        not in available_capacity_tbl.columns
        and
        "DependableMW"
        in available_capacity_tbl.columns
    ):
    
        available_capacity_tbl[
            "AvailableMW"
        ] = (
            available_capacity_tbl[
                "DependableMW"
            ]
        )
    
    return available_capacity_tbl
