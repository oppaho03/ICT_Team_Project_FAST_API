from dotenv import load_dotenv
import os

load_dotenv()

ORACLE_DSN = {
    "user": os.getenv("ORACLE_USER"),
    "password": os.getenv("ORACLE_PASSWORD"),
    "dsn": os.getenv("ORACLE_DSN"),
    "encoding": "UTF-8"
}
