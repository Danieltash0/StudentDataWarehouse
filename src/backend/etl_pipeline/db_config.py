#DB_CONFIG = {
#    "user": "root",
#    "password": "12345",
#    "host": "localhost",
#    "port": 3306,
#    "database": "stud_constellation_dw"
#}


# ============================================================
# db_config.py  —  reads from environment variables so the
# same codebase works both locally and inside Docker.
#
# Local defaults match the original hardcoded values so
# running outside Docker requires no changes.
# ============================================================
import os

DB_CONFIG = {
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", "12345"),
    "host":     os.getenv("DB_HOST",     "localhost"),   # Docker sets this to "mysql"
    "port":     int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME",     "stud_constellation_dw"),
}