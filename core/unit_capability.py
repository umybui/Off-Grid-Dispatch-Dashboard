import pandas as pd


def get_unit_flag(row):

    if pd.isna(row["DependableMW"]):
        return "No Data"

    if row["DependableMW"] <= 0:
        return "Unavailable"

    if row["SustainedCapabilityPct"] >= 80:
        return "OK"

    if row["SustainedCapabilityPct"] >= 40:
        return "Monitor"

    return "Underperforming"


def get_unit_remark(row):

    flag = row["RiskFlag"]

    if flag == "OK":
        return (
            "Frequently sustains at least "
            "80% of dependable capacity."
        )

    if flag == "Monitor":
        return (
            "Moderate sustained capability. "
            "Monitor performance."
        )

    if flag == "Underperforming":
        return (
            "Unit rarely sustained "
            "dependable capability."
        )

    if flag == "Unavailable":
        return (
            "Unit unavailable."
        )

    return ""


def build_unit_capability(
    generation,
    capacity_reference
):

    unit_perf = (
        generation
        .groupby(
            "Plant",
            as_index=False
        )
        .agg(
            AvgMW=("Value", "mean"),
            MaxObservedMW=("Value", "max"),
            EnergyMWh=("Value", "sum"),
            OperatingHours=(
                "Value",
                lambda x: (x > 0).sum()
            )
        )
    )

    unit_perf = (
        unit_perf.merge(
            capacity_reference,
            on="Plant",
            how="left"
        )
    )

    unit_perf["HoursAbove80Pct"] = (
        generation.merge(
            capacity_reference,
            on="Plant",
            how="left"
        )
        .groupby("Plant")
        .apply(
            lambda x:
            (
                x["Value"]
                >=
                x["DependableMW"] * 0.80
            ).sum()
        )
        .values
    )

    unit_perf[
        "UtilizationFactorPct"
    ] = (
        unit_perf["AvgMW"]
        /
        unit_perf["DependableMW"]
        * 100
    )

    unit_perf[
        "CapabilityRealizationPct"
    ] = (
        unit_perf["MaxObservedMW"]
        /
        unit_perf["DependableMW"]
        * 100
    )

    unit_perf[
        "SustainedCapabilityPct"
    ] = (
        unit_perf["HoursAbove80Pct"]
        /
        unit_perf["OperatingHours"]
        * 100
    )

    unit_perf["RiskFlag"] = (
        unit_perf.apply(
            get_unit_flag,
            axis=1
        )
    )

    unit_perf["Remarks"] = (
        unit_perf.apply(
            get_unit_remark,
            axis=1
        )
    )

    return unit_perf
