import pandas as pd


def build_dependable_audit(
    df,
    config
):

    if (
        "Unit"
        not in df.columns
    ):
        return {
            "plant_totals":
                pd.DataFrame(),
            "unit_breakdown":
                pd.DataFrame()
        }

    capacity_df = (
        df[
            df["Attribute"]
            .astype(str)
            .str.upper()
            .isin(
                [
                    "DEPENDABLE CAPACITY",
                    "GUARANTEED DEPENDABLE CAPACITY (KW)"
                ]
            )
        ]
        .copy()
    )

    if capacity_df.empty:

        return {
            "plant_totals":
                pd.DataFrame(),
            "unit_breakdown":
                pd.DataFrame()
        }

    unit_breakdown = (
        capacity_df
        .groupby(
            ["Plant", "Unit"],
            as_index=False
        )["Value"]
        .max()
        .rename(
            columns={
                "Value":
                "DependableMW"
            }
        )
    )

    plant_totals = (
        unit_breakdown
        .groupby(
            "Plant",
            as_index=False
        )["DependableMW"]
        .sum()
    )

    return {

        "plant_totals":
            plant_totals,

        "unit_breakdown":
            unit_breakdown

    }
