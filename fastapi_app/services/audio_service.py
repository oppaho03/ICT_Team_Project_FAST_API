import os
import pandas as pd
from fastapi import UploadFile
from fastapi_app.services.transcribe import transcribe_audio
from fastapi_app.services.analyze_sentiment import sentiment_analysis
from fastapi_app.services.keyword_analysis import load_keywords, keyword_sentiment_analysis

def analyze_audio_and_generate_result(file: UploadFile, upload_dir: str) -> dict:
    # ✅ 업로드 디렉토리 생성 (없으면 자동 생성)
    os.makedirs(upload_dir, exist_ok=True)

    # ✅ 파일 저장 경로 설정
    file_path = os.path.join(upload_dir, file.filename)

    # ✅ 파일 저장
    contents = file.file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # ✅ Whisper로 텍스트 변환
    text = transcribe_audio(file_path)

    # ✅ 감성 분석
    sentiment = sentiment_analysis(text)

    # ✅ 키워드 감성 분석
    keywords = load_keywords()
    keyword_result = keyword_sentiment_analysis(text, keywords)

    # ✅ 결과 딕셔너리
    result = {
        "file_name": file.filename,
        "transcribed_text": text,
        "overall_sentiment": sentiment["sentiment"],
        "overall_score": sentiment["score"],
        "keyword_sentiment": keyword_result
    }

    # ✅ CSV 저장
    output_csv = os.path.join(upload_dir, "api_results.csv")
    df = pd.DataFrame([result])
    df.to_csv(output_csv, index=False, mode="a", header=not os.path.exists(output_csv), encoding="utf-8-sig")

    return result
