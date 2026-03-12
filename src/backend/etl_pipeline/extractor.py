import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

def extract_raw_data():
    """
    Extract data from the merged dataset (studentcombined.csv)
    This dataset contains 382 students with .x and .y columns for Math and Portuguese subjects
    """
    combined_path = DATA_DIR / "studentcombined.csv"
    
    raw_df = pd.read_csv(combined_path, sep=';')
    
    print(f"Extracted {len(raw_df)} rows from merged dataset")
    print("Sample columns:", raw_df.columns.tolist()[:10])  # Show first 10 columns
    
    return raw_df
