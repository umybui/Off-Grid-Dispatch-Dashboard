import pandas as pd


def build_dependable_audit(
    df,
    config
):

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
            "has_unit_data": False,
            "plant_totals": pd.DataFrame(),
            "unit_breakdown": pd.DataFrame()
        }

    # --------------------------------------------------
    # UNIT-LEVEL DATA AVAILABLE
    # --------------------------------------------------

    if (
        "Unit" in capacity_df.columns
        and
        capacity_df["Unit"].notna().any()
    ):

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

            "has_unit_data":
                True,

            "plant_totals":
                plant_totals,

            "unit_breakdown":
                unit_breakdown
        }

    # --------------------------------------------------
    # PLANT-LEVEL ONLY (MINDORO)
    # --------------------------------------------------

    plant_totals = (
        capacity_df
        .groupby(
            "Plant",
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

    return {

        "has_unit_data":
            False,

        "plant_totals":
            plant_totals,

        "unit_breakdown":
            pd.DataFrame()
    }
