import pandas as pd
from sqlalchemy import create_engine
from etl_pipeline.db_config import DB_CONFIG

MYSQL_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)

#Generic table loader
def load_table(df, table_name):
    if df.empty:
        print(f"No data to insert into {table_name}")
        return

    # Deduplicate ONLY dimensions
    if table_name.startswith("dim_"):
        existing = pd.read_sql(f"SELECT * FROM {table_name}", engine)

        if not existing.empty:
            existing = existing.iloc[:, 1:]  # drop surrogate key
            df = df[existing.columns]

            df = (
                df.merge(
                    existing.drop_duplicates(),
                    on=list(existing.columns),
                    how="left",
                    indicator=True
                )
                .query("_merge == 'left_only'")
                .drop(columns=["_merge"])
            )

        if df.empty:
            print(f"No new rows to insert into {table_name}")
            return

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

# Helper to fetch the dim tables
def fetch_dimension(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

#Fact loaders with foreign key resolution
def load_fact_student_performance(df):
    """Load performance fact with proper foreign key resolution"""
    # Get dimension tables for foreign key mapping
    students = fetch_dimension("dim_student")
    subjects = fetch_dimension("dim_subject")
    parents = fetch_dimension("dim_parent_details")
    academic_support = fetch_dimension("dim_academic_support")
    
    # Create foreign key mappings
    student_map = students.set_index([
        'school', 'sex', 'age', 'address', 'famsize', 'pstatus', 'guardian'
    ])['student_id'].to_dict()
    
    subject_map = subjects.set_index('subject_name')['subject_id'].to_dict()
    
    parent_map = parents.set_index([
        'medu', 'fedu', 'mjob', 'fjob'
    ])['parent_details_id'].to_dict()
    
    academic_map = academic_support.set_index([
        'reason', 'schoolsup', 'famsup', 'paid'
    ])['academic_support_id'].to_dict()
    
    # Map foreign keys
    df['student_id'] = df.apply(
        lambda row: student_map.get(
            (row['school'], row['sex'], row['age'], row['address'], 
             row['famsize'], row['pstatus'], row['guardian'])
        ), axis=1
    )
    
    df['subject_id'] = df['subject_name'].map(subject_map)
    df['parent_details_id'] = df.apply(
        lambda row: parent_map.get(
            (row['medu'], row['fedu'], row['mjob'], row['fjob'])
        ), axis=1
    )
    df['academic_support_id'] = df.apply(
        lambda row: academic_map.get(
            (row['reason'], row['schoolsup'], row['famsup'], row['paid'])
        ), axis=1
    )
    
    # Select only fact table columns
    fact_cols = [
        'student_id', 'subject_id', 'parent_details_id', 'academic_support_id',
        'first_period_grade', 'second_period_grade', 'final_grade',
        'prior_class_failures', 'total_absences', 
        'weekly_study_time_category', 'commute_time_category'
    ]
    
    fact_df = df[fact_cols].copy()
    load_table(fact_df, "fact_student_performance")

def load_fact_student_lifestyle(df):
    """Load lifestyle fact with proper foreign key resolution"""
    # Get student dimension for foreign key mapping
    students = fetch_dimension("dim_student")
    
    # Create student foreign key mapping
    student_map = students.set_index([
        'school', 'sex', 'age', 'address', 'famsize', 'pstatus', 'guardian'
    ])['student_id'].to_dict()
    
    # Map student foreign key
    df['student_id'] = df.apply(
        lambda row: student_map.get(
            (row['school'], row['sex'], row['age'], row['address'], 
             row['famsize'], row['pstatus'], row['guardian'])
        ), axis=1
    )
    
    # Select only fact table columns
    fact_cols = [
        'student_id',
        'extracurricular_activities', 'attended_nursery_school', 
        'plans_higher_education', 'internet_access', 'romantic_relationship',
        'family_relationship_quality_score', 'free_time_index', 
        'social_activity_index', 'weekday_alcohol_consumption_level',
        'weekend_alcohol_consumption_level', 'health_status_score'
    ]
    
    fact_df = df[fact_cols].copy()
    load_table(fact_df, "fact_student_lifestyle")
