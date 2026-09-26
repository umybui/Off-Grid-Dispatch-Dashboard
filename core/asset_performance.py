import pandas as pd


def asset_flag(row):

    dependable = row["DependableMW"]

    realization = row[
        "CapabilityRealizationPct"
    ]

    if pd.isna(dependable):
        return "No Data"

    if dependable <= 0:
        return "Unavailable"

    if realization >= 95:
        return "OK"

    if realization >= 75:
        return "Monitor"

    return "Underperforming"


def asset_remark(row):

    flag = row["RiskFlag"]

    if flag == "OK":
        return (
            "Plant achieved available capability "
            "during the study period."
        )

    if flag == "Monitor":
        return (
            "Plant approached available capability "
            "but did not fully realize it."
        )

    if flag == "Underperforming":
        return (
            "Plant never achieved expected capability."
        )

    if flag == "Unavailable":
        return (
            "No available capacity recorded."
        )

    return ""


def build_asset_performance(
    generation,
    capacity_reference
):

    asset_perf = (
        generation
        .groupby(
            "Plant",
            as_index=False
        )
        .agg(
            AvgMW=(
                "Value",
                "mean"
            ),

            MaxObservedMW=(
                "Value",
                "max"
            ),

            EnergyMWh=(
                "Value",
                "sum"
            )
        )
    )

    asset_perf = (
        asset_perf.merge(
            capacity_reference,
            on="Plant",
            how="left"
        )
    )

    asset_perf[
        "UtilizationFactorPct"
    ] = (
        asset_perf["AvgMW"]
        /
        asset_perf["DependableMW"]
        * 100
    )

    asset_perf[
        "CapabilityRealizationPct"
    ] = (
        asset_perf["MaxObservedMW"]
        /
        asset_perf["DependableMW"]
        * 100
    )

    asset_perf[
        "RiskFlag"
    ] = (
        asset_perf.apply(
            asset_flag,
            axis=1
        )
    )

    asset_perf[
        "Remarks"
    ] = (
        asset_perf.apply(
            asset_remark,
            axis=1
        )
    )

    asset_perf = (
        asset_perf.sort_values(
            "CapabilityRealizationPct"
        )
    )

    return asset_perf
