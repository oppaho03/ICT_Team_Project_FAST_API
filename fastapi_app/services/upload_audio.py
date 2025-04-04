import os
import shutil
import requests
import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from keyword_analysis import load_keywords, keyword_sentiment_analysis
from transcribe import transcribe_audio
from analyze_sentiment import sentiment_analysis

router = APIRouter()
UPLOAD_FOLDER = "./audio_data"


@router.post("/api/files/upload_result")
async def upload_file(file: UploadFile = File(...)):
    """오디오 파일을 업로드하고 분석한 후, 결과를 SpringBoot로 전송"""
    try:
        # 1. 파일 저장
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. 음성 텍스트 변환
        text = transcribe_audio(file_path)

        # 3. 감성 분석
        overall_sentiment = sentiment_analysis(text)

        # 4. 키워드 감성 분석
        keywords = load_keywords()
        keyword_results = keyword_sentiment_analysis(text, keywords)

        # 5. 결과 딕셔너리 구성
        result = {
            'file_name': file.filename,
            'transcribed_text': text,
            'overall_sentiment': overall_sentiment['sentiment'],
            'overall_score': overall_sentiment['score'],
            'keyword_sentiment': keyword_results
        }

        # 6. CSV 저장
        df = pd.DataFrame([result])
        output_csv = os.path.join(UPLOAD_FOLDER, 'api_results.csv')
        df.to_csv(output_csv, index=False, mode='a', header=not os.path.exists(output_csv), encoding='utf-8-sig')

        # 7. 결과를 SpringBoot로 전송
        send_results_to_springboot(result)

        # 8. 클라이언트에는 단순 성공 메시지
        return JSONResponse(content={"message": "분석 완료 및 스프링 서버 전송 완료 ✅"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 분석 중 오류 발생: {str(e)}")


# ✅ SpringBoot로 결과 전송하는 함수
def send_results_to_springboot(result_dict):
    url = "http://localhost:8081/api/files/upload_result"  # SpringBoot의 API 주소
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, json=result_dict, headers=headers)
        if response.status_code == 200:
            print("✅ SpringBoot에 성공적으로 전송됨")
        else:
            print(f"❌ SpringBoot 전송 실패: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ SpringBoot 통신 오류: {str(e)}")
