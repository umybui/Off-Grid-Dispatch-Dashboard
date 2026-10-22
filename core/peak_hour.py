import pandas as pd


def build_peak_hour_analysis(
    total_demand,
    generation
):

    peak_demand = (
        total_demand["Value"]
        .max()
    )

    peak_threshold = (
        peak_demand * 0.90
    )

    peak_hours = (
        total_demand.loc[
            total_demand["Value"]
            >= peak_threshold,
            "Datetime"
        ]
    )

    peak_generation = (
        generation[
            generation["Datetime"]
            .isin(peak_hours)
        ]
        .copy()
    )

    peak_snapshot = (
        peak_generation
        .groupby(
            ["Plant", "Unit"],
            as_index=False
        )
        .agg(
            AvgPeakMW=(
                "Value",
                "mean"
            ),

            MaxPeakMW=(
                "Value",
                "max"
            ),

            PeakEnergyMWh=(
                "Value",
                "sum"
            )
        )
    )

    total_peak_energy = (
        peak_snapshot[
            "PeakEnergyMWh"
        ].sum()
    )

    peak_snapshot[
        "PeakEnergySharePct"
            ] = plant_totals = (
            peak_snapshot
            .groupby(
                "Plant",
                as_index=False
            )[
                "PeakEnergySharePct"
            ]
            .sum()
            .rename(
                columns={
                    "PeakEnergySharePct":
                    "PlantSharePct"
                }
            )
        )
        
        peak_snapshot = (
            peak_snapshot
            .merge(
                plant_totals,
                on="Plant",
                how="left"
            )
        )

    peak_snapshot = (
        peak_snapshot
        .sort_values(
            "PeakEnergySharePct",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )

    return {

        "peak_threshold":
            peak_threshold,

        "peak_hours":
            peak_hours,

        "peak_snapshot":
            peak_snapshot

    }
