import csv
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"

def _detect_separator(path: Path) -> str:
    """
    Sniff the separator from the first line of the CSV.
    Handles both comma-separated and semicolon-separated files so the
    pipeline works regardless of how studentcombined.csv was produced.
    """
    with open(path, newline="", encoding="utf-8") as f:
        sample = f.read(4096)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        return dialect.delimiter
    except csv.Error:
        # Fall back to comma if sniffing fails
        return ","

def extract_raw_data():
    """
    Extract data from merged dataset (studentcombined.csv).
    Contains 382 students with .x columns (Math) and .y columns (Portuguese).
    """
    combined_path = DATA_DIR / "studentcombined.csv"
    
    # The CSV has quoted column names but unquoted data rows
    # We need to handle this properly
    try:
        # Read first line to get quoted column names
        with open(combined_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # Extract column names from quotes
        if first_line.startswith('"') and first_line.endswith('"'):
            column_names = first_line[1:-1].split('","')
            print(f"Manually extracted {len(column_names)} columns: {column_names[:5]}...")
            
            # Read the rest of the file with proper column names
            raw_df = pd.read_csv(combined_path, sep=',', quotechar='"', names=column_names, skiprows=1, dtype=str)
        else:
            # Fallback to normal reading
            raw_df = pd.read_csv(combined_path, sep=',', quotechar='"', dtype=str)
        
        print(f"Extracted {len(raw_df)} rows from CSV")
    except Exception as e:
        print(f"CSV extraction failed: {e}")
        # Last resort
        raw_df = pd.read_csv(combined_path, sep=',', dtype=str)
        print(f"Fallback extracted {len(raw_df)} rows")
    
    print(f"Final column count: {len(raw_df.columns)}")
    print("Sample columns:", raw_df.columns.tolist()[:10])
    print("Sample data types:", raw_df.dtypes.to_dict())
    print("Sample row 0:", raw_df.iloc[0].to_dict() if len(raw_df) > 0 else "No data")
    
    return raw_df