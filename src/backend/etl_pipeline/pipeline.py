from etl_pipeline.extractor import extract_raw_data
from etl_pipeline.transformer import (
    transform_data,
    build_dim_student,
    build_dim_subject,
    build_dim_parent_details,
    build_dim_academic_factors,
    build_fact_student_performance,
    build_fact_student_lifestyle
)
from etl_pipeline.loader import (
    load_table,
    load_fact_student_performance,
    load_fact_student_lifestyle,
    fetch_dimension
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
    dim_academic_factors = build_dim_academic_factors(clean_df)

    #load dimensions
    load_table(dim_student, "dim_student")
    load_table(dim_subject, "dim_subject")
    load_table(dim_parent_details, "dim_parent_details")
    load_table(dim_academic_factors, "dim_academic_factors")

    #fetch dimensions
    dim_student_db = fetch_dimension("dim_student")
    dim_subject_db = fetch_dimension("dim_subject")
    dim_parent_db = fetch_dimension("dim_parent_details")
    dim_academic_db = fetch_dimension("dim_academic_factors")

    #Building facts with surrogate keys
    fact_performance = build_fact_student_performance(clean_df)
    fact_lifestyle = build_fact_student_lifestyle(clean_df)

    #merging surrogate keys here

    #STUDENT KEY
    student_cols = [
        "school", "sex", "age",
        "address", "famsize",
        "pstatus", "guardian"
    ]

    fact_performance = fact_performance.merge(
        dim_student_db,
        on=student_cols,
        how="left"
    )

    fact_lifestyle = fact_lifestyle.merge(
        dim_student_db,
        on=student_cols,
        how="left"
    )

    #SUBJECT KEY
    fact_performance = fact_performance.merge(
        dim_subject_db,
        on="subject_name",
        how="left"
    )

    #PARENT DETAILS KEY
    parent_cols = [
        "mother_education_level",
        "father_education_level",
        "mother_job_title",
        "father_job_title"
    ]

    fact_performance = fact_performance.merge(
        dim_parent_db,
        on=parent_cols,
        how="left"
    )

    #ACADEMIC FACTORS KEY
    academic_cols = ["reason", "schoolsup", "famsup", "paid"]

    fact_performance = fact_performance.merge(
        dim_academic_db,
        on=academic_cols,
        how="left"
    )

    #select only fks and measures for final fact tables
    fact_performance_final = fact_performance[
        [
            "student_id",
            "subject_id",
            "parent_details_id",
            "academic_factors_id",
            "first_period_grade",
            "second_period_grade",
            "final_grade",
            "prior_class_failures",
            "total_absences"
        ]
    ]

    fact_lifestyle_final = fact_lifestyle[
        [
            "student_id",
            "commute_time_category",
            "weekly_study_time_category",
            "activities",
            "nursery",
            "higher",
            "internet",
            "romantic",
            "family_relationship_score",
            "free_time_index",
            "social_activity_index",
            "weekday_alcohol_consumption_level",
            "weekend_alcohol_consumption_level",
            "health_status_score"
        ]
    ]

    #Load Facts
    load_fact_student_performance(fact_performance_final)
    load_fact_student_lifestyle(fact_lifestyle_final)

    print("ETL pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
