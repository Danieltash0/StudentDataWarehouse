import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent 
DATA_DIR = BASE_DIR / "data" / "raw"

def extract_raw_data():
    mat_path = DATA_DIR / "student-mat.csv"
    por_path = DATA_DIR / "student-por.csv"

    mat_df = pd.read_csv(mat_path, sep=",")
    por_df = pd.read_csv(por_path, sep=",")

    mat_df["subject_name"] = "Math"
    por_df["subject_name"] = "Portuguese"

    raw_df = pd.concat([mat_df, por_df], ignore_index=True)

    # Debug safety check 
    #print("RAW COLUMNS AFTER EXTRACT:", raw_df.columns.tolist())

    return raw_df
