import pandas as pd


def get_flag(row):

    dependable = row["DependableMW"]

    peak_support = row["PeakSupportPct"]

    if pd.isna(dependable):
        return "No Data"

    if dependable <= 0:
        return "Unavailable"

    if peak_support >= 90:
        return "OK"

    if peak_support >= 70:
        return "Monitor"

    return "Underperforming"


def get_remarks(row):

    flag = row["RiskFlag"]

    if flag == "OK":
        return (
            "Plant achieved expected capability "
            "during peak demand periods."
        )

    if flag == "Monitor":
        return (
            "Plant delivered partial capability "
            "during peak demand periods."
        )

    if flag == "Underperforming":
        return (
            "Plant did not achieve expected "
            "peak demand performance."
        )

    if flag == "Unavailable":
        return (
            "Plant unavailable during the "
            "analysis period."
        )

    return ""


def build_peak_support_table(
    peak_snapshot,
    dependable_capacity
):

    merge_keys = ["Plant"]
    
    if (
        "Unit" in peak_snapshot.columns
        and "Unit" in dependable_capacity.columns
    ):
        merge_keys = [
            "Plant",
            "Unit"
        ]
    
    performance = (
        peak_snapshot.merge(
            dependable_capacity,
            on=merge_keys,
            how="left"
        )
    )
    
    performance["PeakSupportPct"] = (
        performance["MaxPeakMW"]
        /
        performance["DependableMW"]
        * 100
    )

    performance["RiskFlag"] = (
        performance.apply(
            get_flag,
            axis=1
        )
    )

    performance["Remarks"] = (
        performance.apply(
            get_remarks,
            axis=1
        )
    )

    performance = (
        performance.sort_values(
            "PeakSupportPct"
        )
    )

    return performance
