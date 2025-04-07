import oracledb
import os
import json
import logging
from dotenv import load_dotenv

# ✅ .env 환경 변수 로드
load_dotenv()

# ✅ 로거 설정
logger = logging.getLogger(__name__)

# ✅ DB 연결 함수
def get_db_connection():
    oracle_dsn = os.getenv("ORACLE_DSN")
    if not oracle_dsn:
        raise ValueError("❌ ORACLE_DSN 환경변수가 설정되어 있지 않습니다.")
    return oracledb.connect(oracle_dsn)

# ✅ 텍스트 분석 결과 저장 함수
def save_text_processing_result(original_text: str, processed_text: str, keywords: list):
    # 🔹 유효성 검사
    if not original_text or not processed_text:
        raise ValueError("❌ 원본 텍스트나 처리된 텍스트가 비어 있습니다.")

    conn = None
    cursor = None

    try:
        # 🔹 DB 연결 및 커서 생성
        conn = get_db_connection()
        cursor = conn.cursor()

        # 🔹 JSON 데이터 구성
        json_data = json.dumps({
            "original_text": original_text,
            "processed_text": processed_text,
            "keywords": keywords
        }, ensure_ascii=False)

        # 🔹 INSERT 쿼리 실행
        cursor.execute("INSERT INTO text_processing_results (data) VALUES (:1)", [json_data])
        conn.commit()
        print("✅ 텍스트 분석 결과 DB 저장 완료")

        return {"message": "데이터 저장 완료"}

    except Exception as e:
        if conn:
            conn.rollback()
        logger.warning(f"[DB 저장 오류] {e}")
        print(f"[❌ DB 저장 오류] {e}")
        raise

    finally:
        # 🔹 리소스 정리
        if cursor:
            cursor.close()
        if conn:
            conn.close()
