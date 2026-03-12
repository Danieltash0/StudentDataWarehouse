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
    
    # Try reading with proper quote handling first
    try:
        raw_df = pd.read_csv(combined_path, sep=';', quotechar='"')
        print(f"Extracted {len(raw_df)} rows using semicolon separator")
    except Exception as e:
        print(f"Semicolon separator failed: {e}")
        # Fallback to comma
        try:
            raw_df = pd.read_csv(combined_path, sep=',', quotechar='"')
            print(f"Extracted {len(raw_df)} rows using comma separator")
        except Exception as e2:
            print(f"Comma separator failed: {e2}")
            # Last resort - try without quotes
            raw_df = pd.read_csv(combined_path, sep=';')
            print(f"Extracted {len(raw_df)} rows without quote handling")
    
    # Check if we still have only one column (all quoted together)
    if len(raw_df.columns) == 1:
        print("Warning: Still detecting single column, attempting manual parsing...")
        # Read the first line to extract column names
        with open(combined_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        
        # Remove quotes and split by semicolon
        if first_line.startswith('"') and first_line.endswith('"'):
            column_names = first_line[1:-1].split('","')
            print(f"Manually extracted {len(column_names)} columns")
            
            # Re-read with proper column names
            raw_df = pd.read_csv(combined_path, sep=';', quotechar='"', names=column_names, skiprows=1)
    
    print(f"Final column count: {len(raw_df.columns)}")
    print("Sample columns:", raw_df.columns.tolist()[:10])
    
    return raw_df