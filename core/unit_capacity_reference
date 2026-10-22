import pandas as pd


def build_unit_capacity_reference(
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
                    "DEPENDABLE CAPACITY",
                    "GUARANTEED DEPENDABLE CAPACITY (KW)",
                    "INSTALLED CAPACITY (MW)",
                    "INSTALLED CAPACITY (KW)",
                    "AVAILABLE CAPACITY (KW)"
                ]
            )
        ]
        .copy()
    )

    if capacity_data.empty:
        return pd.DataFrame()

    dependable_df = (
        capacity_data[
            capacity_data["Attribute"]
            .astype(str)
            .str.upper()
            .isin(
                [
                    "DEPENDABLE CAPACITY",
                    "GUARANTEED DEPENDABLE CAPACITY (KW)"
                ]
            )
        ]
        .groupby(
            ["Plant", "Unit"],
            as_index=False
        )["Value"]
        .max()
        .rename(
            columns={
                "Value": "DependableMW"
            }
        )
    )

    installed_df = (
        capacity_data[
            capacity_data["Attribute"]
            .astype(str)
            .str.upper()
            .isin(
                [
                    "INSTALLED CAPACITY (MW)",
                    "INSTALLED CAPACITY (KW)"
                ]
            )
        ]
        .groupby(
            ["Plant", "Unit"],
            as_index=False
        )["Value"]
        .max()
        .rename(
            columns={
                "Value": "InstalledMW"
            }
        )
    )

    available_df = (
        capacity_data[
            capacity_data["Attribute"]
            .astype(str)
            .str.upper()
            .eq(
                "AVAILABLE CAPACITY (KW)"
            )
        ]
        .groupby(
            ["Plant", "Unit"],
            as_index=False
        )["Value"]
        .max()
        .rename(
            columns={
                "Value": "AvailableMW"
            }
        )
    )

    capacity_reference = (
        dependable_df
        .merge(
            installed_df,
            on=["Plant", "Unit"],
            how="left"
        )
        .merge(
            available_df,
            on=["Plant", "Unit"],
            how="left"
        )
    )

    if "InstalledMW" not in capacity_reference.columns:
        capacity_reference["InstalledMW"] = (
            capacity_reference["DependableMW"]
        )

    capacity_reference["InstalledMW"] = (
        capacity_reference["InstalledMW"]
        .fillna(
            capacity_reference["DependableMW"]
        )
    )

    capacity_reference["AvailableMW"] = (
        capacity_reference["AvailableMW"]
        .fillna(
            capacity_reference["DependableMW"]
        )
    )

    return capacity_reference
