def filter_data(df, filters):

    # ----------------------------------
    # YEAR FILTER
    # ----------------------------------

    if "Year" in filters:

        df = df[
            df["Datetime"]
            .dt.year
            .isin(filters["Year"])
        ]

    # ----------------------------------
    # MONTH + DAY FILTER
    # ----------------------------------

    filtered = df[
        (
            df["Month"].isin(
                filters["selected_months"]
            )
        )
        &
        (
            df["Day"].isin(
                filters["selected_days"]
            )
        )
    ].copy()

    return filtered
