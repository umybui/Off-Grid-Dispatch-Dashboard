import pandas as pd


def build_demand_generation(filtered, config):

    demand_attribute = config.get(
        "DEMAND_ATTRIBUTE"
    )

    generation_attribute = config.get(
        "GENERATION_ATTRIBUTE"
    )

    demand_plant = config.get(
        "DEMAND_PLANT"
    )

    # ==========================================
    # TOTAL DEMAND
    # ==========================================

    if demand_plant:

        total_demand = (
            filtered[
                (
                    filtered["Plant"]
                    .astype(str)
                    .str.upper()
                    ==
                    demand_plant.upper()
                )
            ]
            .copy()
        )

        if demand_attribute:

            total_demand = (
                total_demand[
                    total_demand["Attribute"]
                    .astype(str)
                    .str.upper()
                    ==
                    demand_attribute.upper()
                ]
            )

    else:

        total_demand = (
            filtered[
                filtered["Attribute"]
                .astype(str)
                .str.upper()
                ==
                demand_attribute.upper()
            ]
            .copy()
        )

    total_demand = (
        total_demand
        .groupby(
            "Datetime",
            as_index=False
        )["Value"]
        .sum()
    )

    # ==========================================
    # GENERATION
    # ==========================================

    generation = (
        filtered[
            filtered["Attribute"]
            .astype(str)
            .str.upper()
            ==
            generation_attribute.upper()
        ]
        .groupby(
            ["Datetime", "Plant"],
            as_index=False
        )["Value"]
        .sum()
    )

    if demand_plant:

        generation = generation[
            generation["Plant"]
            .astype(str)
            .str.upper()
            != demand_plant.upper()
        ]

    # ==========================================
    # TOTAL GENERATION
    # ==========================================

    total_generation = (
        generation
        .groupby(
            "Datetime",
            as_index=False
        )["Value"]
        .sum()
    )

    total_generation.rename(
        columns={
            "Value":
            "TotalGeneration"
        },
        inplace=True
    )

    return (
        total_demand,
        generation,
        total_generation
    )
