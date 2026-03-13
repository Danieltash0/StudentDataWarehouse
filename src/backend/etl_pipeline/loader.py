import pandas as pd
from sqlalchemy import create_engine, text
from etl_pipeline.db_config import DB_CONFIG

MYSQL_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)
engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)


def clear_all_tables():
    """Clear all tables in reverse dependency order to prevent FK violations."""
    print("Clearing existing data...")
    tables_to_clear = [
        "fact_student_performance",
        "fact_student_lifestyle",
        "dim_academic_support",
        "dim_parent_details",
        "dim_subject",
        "dim_student",
    ]
    with engine.begin() as conn:
        for table in tables_to_clear:
            conn.execute(text(f"DELETE FROM {table}"))
            print(f"  Cleared {table}")


def load_table(df, table_name):
    """Bulk-load a DataFrame into a table using pandas .to_sql()."""
    if df.empty:
        print(f"  No data to insert into {table_name}")
        return 0

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )
    print(f"  Loaded {len(df)} rows into {table_name}")
    return len(df)


def fetch_dimension(table_name):
    """Fetch a dimension table for FK mapping."""
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)


def load_fact_student_performance(df):
    """
    Load performance fact with FK resolution for parent_details and
    academic_support dimensions.

    student_id is already set in the DataFrame (set by the transformer
    directly from the row index), so no student composite-key lookup needed.
    """
    print("Loading fact_student_performance....")
    
    # --- Resolve subject FK ---
    subjects = fetch_dimension("dim_subject")
    subject_map = subjects.set_index("subject_name")["subject_id"].to_dict()
    df["subject_id"] = df["subject_name"].map(subject_map)

    # --- Resolve parent_details FK ---
    parents = fetch_dimension("dim_parent_details")
    parent_map = parents.set_index([
        "mother_education_level", "father_education_level",
        "mother_job_title", "father_job_title",
    ])["parent_details_id"].to_dict()

    df["parent_details_id"] = df.apply(
        lambda row: parent_map.get((
            row["mother_education_level"], row["father_education_level"],
            row["mother_job_title"], row["father_job_title"],
        )),
        axis=1,
    )

    # --- Resolve academic_support FK ---
    academic_support = fetch_dimension("dim_academic_support")
    academic_map = academic_support.set_index([
        "school_choice_reason", "school_support",
        "family_support", "extra_paid_classes",
    ])["academic_support_id"].to_dict()

    df["academic_support_id"] = df.apply(
        lambda row: academic_map.get((
            row["school_choice_reason"], row["school_support"],
            row["family_support"], row["extra_paid_classes"],
        )),
        axis=1,
    )

    # --- Validate required FKs ---
    missing_student_fks = df["student_id"].isnull().sum()
    missing_subject_fks = df["subject_id"].isnull().sum()
    missing_parent_fks = df["parent_details_id"].isnull().sum()
    missing_academic_fks = df["academic_support_id"].isnull().sum()
    
    if missing_student_fks > 0:
        print(f"  ERROR: {missing_student_fks} missing student_id values")
    if missing_subject_fks > 0:
        print(f"  ERROR: {missing_subject_fks} missing subject_id values")
    if missing_parent_fks > 0:
        print(f"  ERROR: {missing_parent_fks} missing parent_details_id values")
    if missing_academic_fks > 0:
        print(f"  ERROR: {missing_academic_fks} missing academic_support_id values")

    total_missing = missing_student_fks + missing_subject_fks + missing_parent_fks + missing_academic_fks
    if total_missing > 0:
        print(f"  WARNING: {total_missing} total missing foreign keys")
        # Don't fail the entire load, but log the issue

    # --- Select only fact table columns ---
    fact_cols = [
        "student_id", "subject_id", "parent_details_id", "academic_support_id",
        "first_period_grade", "second_period_grade", "final_grade",
        "prior_class_failures", "total_absences",
        "weekly_study_time_category", "commute_time_category",
    ]
    fact_df = df[fact_cols].copy()
    return load_table(fact_df, "fact_student_performance")


def load_fact_student_lifestyle(df):
    """
    Load lifestyle fact.

    student_id is already set in the DataFrame (set by the transformer
    directly from the row index), so no student composite-key lookup needed.
    """
    print("Loading fact_student_lifestyle...")

    # --- Validate student_id ---
    if df["student_id"].isnull().any():
        raise ValueError(
            f"Missing student_id in lifestyle fact: "
            f"{df['student_id'].isnull().sum()} null rows"
        )

    # --- Select only fact table columns ---
    fact_cols = [
        "student_id",
        "extracurricular_activities", "attended_nursery_school",
        "plans_higher_education", "internet_access", "romantic_relationship",
        "family_relationship_quality_score", "free_time_index",
        "social_activity_index", "weekday_alcohol_consumption_level",
        "weekend_alcohol_consumption_level", "health_status_score",
    ]
    fact_df = df[fact_cols].copy()
    return load_table(fact_df, "fact_student_lifestyle")


def get_table_counts():
    """Return row counts for all warehouse tables."""
    counts = {}
    tables = [
        "dim_student", "dim_subject", "dim_parent_details",
        "dim_academic_support", "fact_student_lifestyle", "fact_student_performance",
    ]
    for table in tables:
        try:
            result = pd.read_sql(f"SELECT COUNT(*) as count FROM {table}", engine)
            counts[table] = int(result["count"].iloc[0])
        except Exception as e:
            counts[table] = f"Error: {e}"
    return counts