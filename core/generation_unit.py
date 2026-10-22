import pandas as pd


def build_generation_unit(
    filtered,
    config
):

    generation_attribute = config.get(
        "GENERATION_ATTRIBUTE"
    )

    plant_column = config.get(
        "PLANT_COLUMN",
        "Plant"
    )

    generation_unit = (
        filtered[
            filtered["Attribute"]
            .astype(str)
            .str.upper()
            ==
            generation_attribute.upper()
        ]
        .copy()
    )

    if (
        config.get(
            "SYSTEM_NAME"
        )
        ==
        "Palawan"
    ):

        generation_unit["Value"] = (
            pd.to_numeric(
                generation_unit[
                    "NumericValue"
                ],
                errors="coerce"
            )
        )

    else:

        generation_unit["Value"] = (
            pd.to_numeric(
                generation_unit[
                    "Value"
                ],
                errors="coerce"
            )
        )

    keep_cols = [
        c
        for c in [
            "Datetime",
            plant_column,
            "Unit",
            "Value"
        ]
        if c in generation_unit.columns
    ]

    generation_unit = (
        generation_unit[
            keep_cols
        ]
        .copy()
    )

    generation_unit.rename(
        columns={
            plant_column:
            "Plant"
        },
        inplace=True
    )

    demand_plant = config.get(
        "DEMAND_PLANT"
    )
    
    if demand_plant:
    
        generation_unit = generation_unit[
            generation_unit["Plant"]
            .astype(str)
            .str.upper()
            != demand_plant.upper()
        ]
    
    exclude_keywords = config.get(
        "GENERATION_EXCLUDE_KEYWORDS",
        []
    )

    if exclude_keywords:

        pattern = "|".join(
            exclude_keywords
        )

        generation_unit = (
            generation_unit[
                ~generation_unit[
                    "Plant"
                ]
                .astype(str)
                .str.contains(
                    pattern,
                    case=False,
                    na=False
                )
            ]
        )

    return generation_unit
