import pandas as pd
from sqlalchemy import create_engine
from etl_pipeline.db_config import DB_CONFIG

MYSQL_URL = (
    f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)


def load_table(df, table_name):
    if df.empty:
        return

    df.to_sql(
        table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi"
    )


def load_fact_student_performance(df):
    load_table(df, "fact_student_performance")


def load_fact_student_lifestyle(df):
    load_table(df, "fact_student_lifestyle")
