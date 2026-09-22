def prepare_data(df):

    df = df.copy()

    df["Datetime"] = df["Datetime"].astype("datetime64[ns]")

    df["NumericValue"] = (
        df["NumericValue"]
        .apply(lambda x: x)
    )

    df["Value"] = df["NumericValue"]

    df["Month"] = df["Datetime"].dt.month

    df["Day"] = df["Datetime"].dt.day

    return df
