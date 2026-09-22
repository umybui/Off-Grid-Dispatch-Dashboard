import pandas as pd

def load_data(config):

    print("CONFIG RECEIVED:", config)

    df = pd.read_excel(
        config["FILE_PATH"],
        sheet_name=config["SHEET_NAME"],
        engine="openpyxl"
    )

    return df
