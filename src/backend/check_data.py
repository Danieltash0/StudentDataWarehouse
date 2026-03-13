import pandas as pd
from sqlalchemy import create_engine, text
from etl_pipeline.db_config import DB_CONFIG

MYSQL_URL = f'mysql+pymysql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'
engine = create_engine(MYSQL_URL, echo=False, pool_pre_ping=True)

parents = pd.read_sql('SELECT * FROM dim_parent_details LIMIT 5', engine)
print('Parent dimension sample:')
print(parents[['mother_education_level', 'father_education_level', 'mother_job_title', 'father_job_title']].head())
print('Data types:')
print(parents.dtypes)
