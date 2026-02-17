from sqlalchemy import create_engine
from .config import DB_CONFIG

def get_engine():
    return create_engine(
f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
        f"{DB_CONFIG['host']}/{DB_CONFIG['database']}"
    )