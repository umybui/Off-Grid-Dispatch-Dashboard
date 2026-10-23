def filter_data(df, filters):

    filtered = df[
        if "Year" in filters:
        
            df = df[
                df["Datetime"]
                .dt.year
                .isin(filters["Year"])
            ]
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
