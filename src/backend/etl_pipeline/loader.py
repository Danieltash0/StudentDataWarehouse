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

    #print(f"Inserted {len(df)} rows into {table_name}")


# Helper to fetch the dim tables
def fetch_dimension(table_name):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)


#Fact loaders
def load_fact_student_performance(df):
    load_table(df, "fact_student_performance")


def load_fact_student_lifestyle(df):
    load_table(df, "fact_student_lifestyle")
