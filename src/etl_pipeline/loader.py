import pandas as pd
from sqlalchemy import text
from typing import List


def load_table(engine, df: pd.DataFrame, table_name: str):
    if df is None or df.empty:
        return

    df_to_load = df.drop_duplicates().copy()

    if df_to_load.empty:
        return

    df_to_load.to_sql(table_name, engine, if_exists="append", index=False)


def clear_tables(engine, table_names: List[str]):
    with engine.begin() as conn:
        if engine.dialect.name == "mysql":
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            for table in table_names:
                conn.execute(text(f"TRUNCATE TABLE {table}"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        else:
            for table in table_names:
                conn.execute(text(f"DELETE FROM {table}"))

