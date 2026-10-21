import pandas as pd


def build_historical_dispatch(
    generation,
    total_demand
):

    plant_generation = (
        generation
        .groupby("Plant", as_index=False)
        ["MW"]
        .mean()
        .rename(
            columns={
                "MW": "AverageMW"
            }
        )
        .sort_values(
            "AverageMW",
            ascending=False
        )
    )

    plant_generation[
        "Priority"
    ] = range(
        1,
        len(plant_generation) + 1
    )

    dispatch_order = (
        plant_generation[
            [
                "Priority",
                "Plant"
            ]
        ]
    )

    return {
        "generation": generation,
        "total_demand": total_demand,
        "dispatch_order": dispatch_order
    }
