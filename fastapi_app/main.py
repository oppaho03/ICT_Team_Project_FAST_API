from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from services.upload_audio import router as stt_router
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi_app.services import openai_service
from fastapi_app.services.openai_service import OpenAIService
from services.ocr_service import OCRService
from services.text_processing_service import TextProcessingService

# .env 로딩
load_dotenv()
# FastAPI 앱 생성
app = FastAPI()
# 감정분석 라우터
app.include_router(stt_router)
# 서비스 인스턴스 생성
ocr_service = OCRService()
openai_service = OpenAIService()
text_processor = TextProcessingService()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 도메인 지정 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OCR API
@app.post("/ocr")
async def ocr_test(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "filesize": len(contents)
    }

@app.post("/ocr_analyze")
async def ocr_and_analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    ocr_result = ocr_service.run_ocr_from_bytes(image_bytes)

    ocr_text = "\n".join(ocr_result)
    openai_response = openai_service.ask_about_prescription(ocr_text)

    return {
        "ocr_raw": ocr_text,
        "gpt_analysis": openai_response
    }

# 텍스트 처리용 모델
class TextRequest(BaseModel):
    text: str

# 텍스트 처리 API
@app.post("/keyword_parser")
def process_text(request: TextRequest):
    result = text_processor.process_text(request.text)
    return result

# API 라우터 등록
@app.get("/")
def read_root():
    return {"message": "음성 분석 API 서버가 실행 중입니다!"}


# 분석 결과를 스프링부트 API로 전송하는 함수
def send_results_to_springboot(post_id, stt_result, sentiment_score):
    url = "http://localhost:8081/api/files/upload_result"  # 스프링부트에서 제공하는 API 엔드포인트
    headers = {'Content-Type': 'application/json'}
    data = {
        "postId": post_id,
        "sttResult": stt_result,
        "sentimentScore": sentiment_score
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("결과가 스프링부트 서버에 성공적으로 전송되었습니다.")
    else:
        print("스프링부트 서버로 결과 전송에 실패했습니다.", response.text)




# 상태 확인 API
@app.get("/test")
def test_api():
    return {"message": "정상 작동중입니다 ! ! ! !"}



# FastAPI 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.65", port=8001)



# 서버 실행 방법
# uvicorn main:app --host 192.168.0.65 --port 8001 --reload
