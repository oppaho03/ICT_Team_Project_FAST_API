import oracledb
import os
import json
from dotenv import load_dotenv

# .env 환경 변수 로드
load_dotenv()

def get_db_connection():
    oracle_dsn = os.getenv("ORACLE_DSN")  # .env에서 DSN 값 불러오기
    if not oracle_dsn:
        raise ValueError("ORACLE_DSN 환경변수가 설정되어 있지 않습니다.")
    return oracledb.connect(oracle_dsn)

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
