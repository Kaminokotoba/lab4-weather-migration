import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/weather_db"
)
MYSQL_DATABASE_URL = os.getenv(
    "MYSQL_DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/weather_db"
)
ECHO_SQL = os.getenv("ECHO_SQL", "false").lower() == "true"