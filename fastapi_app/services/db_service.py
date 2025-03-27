import oracledb
from config import ORACLE_DSN
import json

def get_db_connection():
    return oracledb.connect(ORACLE_DSN)

def save_text_processing_result(original_text: str, processed_text: str, keywords: list):
    conn = get_db_connection()
    cursor = conn.cursor()

    json_data = json.dumps({
        "original_text": original_text,
        "processed_text": processed_text,
        "keywords": keywords
    })

    cursor.execute("INSERT INTO text_processing_results (data) VALUES (:1)", [json_data])
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "데이터 저장 완료"}
