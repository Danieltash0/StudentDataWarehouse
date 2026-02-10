import pandas as pd
from sqlalchemy import create_engine, text
from etl_pipeline.db_config import DB_CONFIG

MYSQL_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True, future=True)

def load_table(df, table_name, unique_cols=None):
    
    if df.empty:
        print(f"DataFrame for {table_name} is empty. Skipping load.")
        return

    df = df.drop_duplicates()
    print(f"Loading {len(df)} rows into {table_name}")

    if unique_cols:
       
        existing_df = pd.read_sql(f"SELECT {', '.join(unique_cols)} FROM {table_name}", engine)
        df = df.merge(existing_df, how="left", indicator=True, on=unique_cols)
        df = df[df["_merge"] == "left_only"].drop(columns="_merge")

        if df.empty:
            print(f"No new rows to insert into {table_name}")
            return

    df.to_sql(
        table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=500
    )

    print(f"Finished loading {table_name}")


def load_fact_student_performance(df):
    """
    Build the fact_student_performance table with foreign keys.
    """
    print("Preparing fact_student_performance table...")

    dim_student = pd.read_sql("SELECT * FROM dim_student", engine)
    dim_family  = pd.read_sql("SELECT * FROM dim_family", engine)
    dim_school  = pd.read_sql("SELECT * FROM dim_school", engine)
    dim_subject = pd.read_sql("SELECT * FROM dim_subject", engine)

    fact_df = df.copy()

    fact_df = fact_df.rename(columns={"school": "school_code"})
    # Merge to get student_id and other foreign keys
    fact_df = fact_df.merge(
        dim_student,
        on=['sex','age','address','guardian','romantic'],
        how='left'
    )

    fact_df = fact_df.merge(
        dim_family,
        left_on=['famsize','pstatus','medu','fedu','mjob','fjob','famrel','famsup'],
        right_on=['famsize','pstatus','medu','fedu','mjob','fjob','famrel','famsup'],
        how='left'
    )

    fact_df = fact_df.merge(
        dim_school,
        left_on=['school_code','reason','schoolsup','paid','activities','nursery','higher','internet'],
        right_on=['school_code','reason','schoolsup','paid','activities','nursery','higher','internet'],
        how='left'
    )

    fact_df = fact_df.merge(
        dim_subject,
        on='subject_name',
        how='left'
    )

    fact_final = fact_df[[
        'student_id', 'family_id', 'school_id', 'subject_id',
        'traveltime', 'studytime', 'failures', 'freetime', 'goout',
        'dalc', 'walc', 'health', 'absences', 'g1', 'g2', 'g3'
    ]]

    load_table(fact_final, "fact_student_performance")
