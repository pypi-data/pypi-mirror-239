import pandas as pd

def load_file_to_dataframe(file_path, file_format):
    if file_format == "csv":
        df = pd.read_csv(file_path)
    elif file_format == "excel":
        df = pd.read_excel(file_path)

    return df
