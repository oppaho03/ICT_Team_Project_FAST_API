import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.stt.transcribe import transcribe_audio
from services.sentiment_analysis.analyze_sentiment import sentiment_analysis
from services.sentiment_analysis.keyword_analysis import keyword_sentiment_analysis, load_keywords
import pandas as pd

router = APIRouter()
UPLOAD_FOLDER = "./audio_data"


@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """오디오 파일을 업로드하고 분석하는 API"""
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 음성을 텍스트로 변환
        text = transcribe_audio(file_path)

        # 감성 분석 수행
        overall_sentiment = sentiment_analysis(text)

        # 키워드 감성 분석
        keywords = load_keywords()
        keyword_results = keyword_sentiment_analysis(text, keywords)

        # 분석 결과
        result = {
            'file_name': file.filename,
            'transcribed_text': text,
            'overall_sentiment': overall_sentiment['sentiment'],
            'overall_score': overall_sentiment['score'],
            'keyword_sentiment': keyword_results
        }

        # CSV 파일 저장
        df = pd.DataFrame([result])
        output_csv = os.path.join(UPLOAD_FOLDER, 'api_results.csv')
        df.to_csv(output_csv, index=False, mode='a', header=not os.path.exists(output_csv), encoding='utf-8-sig')

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 분석 중 오류 발생: {str(e)}")
