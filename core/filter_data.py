def filter_data(df, filters):

    filtered = df.copy()

    # ----------------------------------
    # YEAR
    # ----------------------------------

    filtered = filtered[
        filtered["Datetime"]
        .dt.year
        .isin(
            filters["selected_years"]
        )
    ]

    # ----------------------------------
    # MINDORO AREA
    # ----------------------------------
    
    if (
        "WorkbookSource" in filtered.columns
        and
        len(
            filters["selected_areas"]
        ) > 0
    ):
    
        mask = False
    
        if (
            "Oriental Mindoro"
            in filters["selected_areas"]
        ):
    
            mask = (
                mask
                |
                filtered["WorkbookSource"]
                .astype(str)
                .str.contains(
                    "Oriental Mindoro",
                    case=False,
                    na=False
                )
            )
    
        if (
            "Occidental Mindoro"
            in filters["selected_areas"]
        ):
    
            mask = (
                mask
                |
                filtered["WorkbookSource"]
                .astype(str)
                .str.contains(
                    "Occidental Mindoro",
                    case=False,
                    na=False
                )
            )
    
        filtered = filtered[mask]
    # ----------------------------------
    # MONTH + DAY
    # ----------------------------------

    filtered = filtered[
        (
            filtered["Month"]
            .isin(
                filters["selected_months"]
            )
        )
        &
        (
            filtered["Day"]
            .isin(
                filters["selected_days"]
            )
        )
    ].copy()

    return filtered
