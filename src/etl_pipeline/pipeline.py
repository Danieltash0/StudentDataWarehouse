from etl_pipeline.extractor import extract_raw_data
from etl_pipeline.transformer import (
    transform_data, 
    build_dim_student, 
    build_dim_subject, 
    build_dim_family, 
    build_dim_school
)
from etl_pipeline.loader import load_table, load_fact_student_performance

def run_pipeline():
    print("Starting ETL pipeline")

    raw_df = extract_raw_data()
    print("RAW COLUMNS AFTER EXTRACT:", list(raw_df.columns))

    clean_df = transform_data(raw_df)
    print("RAW COLUMNS:", list(clean_df.columns))

    dim_student = build_dim_student(clean_df)
    dim_subject = build_dim_subject(clean_df)
    dim_family  = build_dim_family(clean_df)
    dim_school  = build_dim_school(clean_df)

    load_table(
        dim_student, 
        "dim_student", 
        unique_cols=["sex","age","address","guardian","romantic"]
    )
    load_table(
        dim_subject, 
        "dim_subject", 
        unique_cols=["subject_name"]
    )
    load_table(
        dim_family, 
        "dim_family", 
        unique_cols=["famsize","pstatus","medu","fedu","mjob","fjob","famrel","famsup"]
    )
    load_table(
        dim_school, 
        "dim_school", 
        unique_cols=["school_code"]
    )

    load_fact_student_performance(clean_df)

    print("ETL pipeline completed")

if __name__ == "__main__":
    run_pipeline()
