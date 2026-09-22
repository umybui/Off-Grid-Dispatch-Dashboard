def filter_data(df, filters):

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
