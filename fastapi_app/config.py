from dotenv import load_dotenv
import os

load_dotenv()

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_DSN = os.getenv("ORACLE_DSN")  # 예: "localhost:1521/orclpdb"
ORACLE_ENCODING = "UTF-8"