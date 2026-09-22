import pandas as pd

def load_data(config):

    df = pd.read_excel(
        config["FILE_PATH"],
        sheet_name=config["SHEET_NAME"]
    )

    return df
