import pandas as pd

def prepare_data(df, config):

    df = df.copy()

    datetime_column = config["DATETIME_COLUMN"]

    value_column = config["VALUE_COLUMN"]

    df["Datetime"] = pd.to_datetime(
        df[datetime_column],
        errors="coerce"
    )

    df["Value"] = pd.to_numeric(
        df[value_column],
        errors="coerce"
    )

    scale = config.get("UNIT_SCALE", 1)

    df["Value"] = (
        pd.to_numeric(
            df[value_column],
            errors="coerce"
        )
        / scale
    )

    df["Month"] = df["Datetime"].dt.month

    df["Day"] = df["Datetime"].dt.day

    return df
