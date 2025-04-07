import os
import shutil
import pandas as pd
from fastapi import UploadFile
from fastapi_app.services.transcribe import transcribe_audio
from fastapi_app.services.analyze_sentiment import sentiment_analysis
from fastapi_app.services.keyword_analysis import load_keywords, keyword_sentiment_analysis


def analyze_audio_and_generate_result(file: UploadFile, upload_dir: str) -> dict:
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = transcribe_audio(file_path)
    sentiment = sentiment_analysis(text)
    keywords = load_keywords()
    keyword_result = keyword_sentiment_analysis(text, keywords)

    result = {
        'file_name': file.filename,
        'transcribed_text': text,
        'overall_sentiment': sentiment['sentiment'],
        'overall_score': sentiment['score'],
        'keyword_sentiment': keyword_result
    }

    output_csv = os.path.join(upload_dir, 'api_results.csv')
    df = pd.DataFrame([result])
    df.to_csv(output_csv, index=False, mode='a', header=not os.path.exists(output_csv), encoding='utf-8-sig')

    return result