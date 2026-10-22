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

    plant_column = config.get(
        "PLANT_COLUMN",
        "Plant"
    )

    # ==========================================
    # TOTAL DEMAND
    # ==========================================

    if demand_plant:

        total_demand = (
            filtered[
                filtered[plant_column]
                .astype(str)
                .str.upper()
                ==
                demand_plant.upper()
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

    generation_raw = (
        filtered[
            filtered["Attribute"]
            .astype(str)
            .str.upper()
            ==
            generation_attribute.upper()
        ]
        .copy()
    )

    # ------------------------------------------
    # PLANT-LEVEL GENERATION
    # ------------------------------------------

    generation = (
        generation_raw
        .groupby(
            ["Datetime", plant_column],
            as_index=False
        )["Value"]
        .sum()
    )

    # ------------------------------------------
    # UNIT-LEVEL GENERATION
    # ------------------------------------------

    if "Unit" in generation_raw.columns:

        generation_unit = (
            generation_raw[
                [
                    "Datetime",
                    plant_column,
                    "Unit"
                ]
            ]
            .copy()
        )
        
        generation_unit["Value"] = (
            generation_raw["NumericValue"]
            if "NumericValue" in generation_raw.columns
            else generation_raw["Value"]
        )
        
    else:

        generation_unit = (
            generation_raw[
                [
                    "Datetime",
                    plant_column,
                    "Value"
                ]
            ]
            .copy()
        )

    # ------------------------------------------
    # REMOVE DEMAND PLANT IF NEEDED
    # ------------------------------------------

    if demand_plant:

        generation = generation[
            generation[plant_column]
            .astype(str)
            .str.upper()
            != demand_plant.upper()
        ]

        generation_unit = generation_unit[
            generation_unit[plant_column]
            .astype(str)
            .str.upper()
            != demand_plant.upper()
        ]

    # ------------------------------------------
    # EXCLUDED GENERATION PLANTS
    # ------------------------------------------

    exclude_keywords = config.get(
        "GENERATION_EXCLUDE_KEYWORDS",
        []
    )

    if exclude_keywords:

        pattern = "|".join(
            exclude_keywords
        )

        generation = generation[
            ~generation[
                plant_column
            ]
            .astype(str)
            .str.contains(
                pattern,
                case=False,
                na=False
            )
        ]

        generation_unit = generation_unit[
            ~generation_unit[
                plant_column
            ]
            .astype(str)
            .str.contains(
                pattern,
                case=False,
                na=False
            )
        ]

    # ==========================================
    # IMPORT SUPPORT
    # ==========================================

    transfer_flow = pd.DataFrame(
        {
            "Datetime": [],
            "ImportSupport": []
        }
    )

    if config.get(
        "USES_IMPORT_SUPPORT",
        False
    ):

        import_keyword = config.get(
            "IMPORT_KEYWORD",
            "IMPORT"
        )

        transfer_rows = filtered[
            filtered[plant_column]
            .astype(str)
            .str.contains(
                import_keyword,
                case=False,
                na=False
            )
        ].copy()

        if not transfer_rows.empty:

            transfer_rows[
                "ImportSupport"
            ] = (
                transfer_rows["Value"]
                .clip(lower=0)
            )

            transfer_flow = (
                transfer_rows
                .groupby(
                    "Datetime",
                    as_index=False
                )["ImportSupport"]
                .sum()
            )

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

    generation.rename(
        columns={
            plant_column:
            "Plant"
        },
        inplace=True
    )

    generation_unit.rename(
        columns={
            plant_column:
            "Plant"
        },
        inplace=True
    )

    return (
        total_demand,
        generation,
        generation_unit,
        total_generation,
        transfer_flow
    )
