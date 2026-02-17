from .extractor import extract_data
from .transformer import (
    transform_data,
    build_dimensions,
    build_family_dimension,
    build_student_dimension,
    build_fact_table,
)
from .loader import load_table, clear_tables
from .db import get_engine
from .config import RESET_DB_ON_RUN

#to ensure this script is being run directly and not imported as module
print("PIPELINE MODULE LOADED")

def run_pipeline():
    print("Starting ETL...")

    engine = get_engine()

    if RESET_DB_ON_RUN:
        clear_tables(
            engine,
            [
                "fact_student_performance",
                "dim_student",
                "dim_family",
                "dim_school",
                "dim_subject",
                "dim_region",
                "dim_guardian",
                "dim_location",
                "dim_parent_job",
                "dim_parent_education",
            ],
        )

    df = extract_data()
    print("Data extracted")

    df = transform_data(df)
    print("Data transformed")

    dims = build_dimensions(df)
    print("Dimensions built")

    for name, table in dims.items():
        load_table(engine, table, name)
        print(f"{name} loaded")

    dim_family = build_family_dimension(df, engine)
    load_table(engine, dim_family, "dim_family")
    print("dim_family loaded")

    dim_student = build_student_dimension(df, engine)
    load_table(engine, dim_student, "dim_student")
    print("dim_student loaded")

    fact = build_fact_table(df, engine)
    
    if fact is not None and not fact.empty:
        load_table(engine, fact, "fact_student_performance")
        print("Fact table loaded")
    else:
        print("Fact table is empty or None")

    print("ETL completed successfully")

if __name__ == "__main__":
    run_pipeline()