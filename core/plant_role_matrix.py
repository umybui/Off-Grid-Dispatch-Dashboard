import pandas as pd


def classify_role(row):

    energy_share = row["EnergySharePct"]

    peak_share = row["PeakSharePct"]

    if (
        energy_share >= 20
        and
        peak_share >= 20
    ):
        return "Critical Support"

    if energy_share >= 20:
        return "Baseload"

    if peak_share >= 15:
        return "Peaking"

    if energy_share >= 5:
        return "Mid-Merit"

    return "Reserve Support"


def build_plant_role_matrix(
    asset_performance,
    peak_snapshot
):

    role_df = (
        asset_performance[
            [
                "Plant",
                "EnergyMWh"
            ]
        ]
        .copy()
    )

    total_energy = (
        role_df["EnergyMWh"]
        .sum()
    )

    role_df["EnergySharePct"] = (
        role_df["EnergyMWh"]
        /
        total_energy
        * 100
    )

    peak_df = (
        peak_snapshot
        .groupby(
            "Plant",
            as_index=False
        )
        .agg(
            PeakEnergySharePct=(
                "PeakEnergySharePct",
                "sum"
            )
        )
    )

    peak_df.rename(
        columns={
            "PeakEnergySharePct":
                "PeakSharePct"
        },
        inplace=True
    )

    role_df = (
        role_df.merge(
            peak_df,
            on="Plant",
            how="left"
        )
    )

    role_df["PeakSharePct"] = (
        role_df["PeakSharePct"]
        .fillna(0)
    )

    x_mid = role_df["PeakSharePct"].median()
    y_mid = role_df["EnergySharePct"].median()
    
    def classify_role(row):
    
        if (
            row["EnergySharePct"] >= y_mid
            and
            row["PeakSharePct"] >= x_mid
        ):
            return "Core Asset"
    
        if (
            row["EnergySharePct"] >= y_mid
            and
            row["PeakSharePct"] < x_mid
        ):
            return "Baseload Asset"
    
        if (
            row["EnergySharePct"] < y_mid
            and
            row["PeakSharePct"] >= x_mid
        ):
            return "Peaking Asset"
    
        return "Support Asset"
    
    role_df["Role"] = (
        role_df.apply(
            classify_role,
            axis=1
        )
    )

    role_df = (
        role_df.sort_values(
            [
                "EnergySharePct",
                "PeakSharePct"
            ],
            ascending=False
        )
    )

    return role_df
