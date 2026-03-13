import pandas as pd
from sqlalchemy import create_engine, text
from etl_pipeline.db_config import DB_CONFIG

MYSQL_URL = f'mysql+pymysql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'
engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)

academic = pd.read_sql('SELECT * FROM dim_academic_support LIMIT 5', engine)
print('Academic support dimension sample:')
print(academic[['school_choice_reason', 'school_support', 'family_support', 'extra_paid_classes']].head())
print('Data types:')
print(academic.dtypes)
