from etl_pipeline.extractor import extract_raw_data
from etl_pipeline.transformer import (
    transform_data,
    build_dim_student,
    build_dim_subject,
    build_dim_parent_details,
    build_dim_academic_support,
    build_fact_student_performance,
    build_fact_student_lifestyle
)
from etl_pipeline.loader import (
    load_table,
    load_fact_student_performance,
    load_fact_student_lifestyle
)

def run_pipeline():
    print("Starting ETL pipeline...")

    #Extract and transform
    raw_df = extract_raw_data()
    clean_df = transform_data(raw_df)

    #build dimensions
    dim_student = build_dim_student(clean_df)
    dim_subject = build_dim_subject(clean_df)
    dim_parent_details = build_dim_parent_details(clean_df)
    dim_academic_support = build_dim_academic_support(clean_df)

    #load dimensions first (required for foreign key resolution)
    print("Loading dimensions...")
    load_table(dim_student, "dim_student")
    load_table(dim_subject, "dim_subject")
    load_table(dim_parent_details, "dim_parent_details")
    load_table(dim_academic_support, "dim_academic_support")

    #Building facts
    print("Building fact tables...")
    fact_performance = build_fact_student_performance(clean_df)
    fact_lifestyle = build_fact_student_lifestyle(clean_df)

    #Load facts (loader handles foreign key resolution)
    print("Loading fact tables...")
    load_fact_student_performance(fact_performance)
    load_fact_student_lifestyle(fact_lifestyle)

    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()
