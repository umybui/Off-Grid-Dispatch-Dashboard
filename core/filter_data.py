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
