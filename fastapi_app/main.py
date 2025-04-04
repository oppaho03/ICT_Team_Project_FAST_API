from dotenv import load_dotenv
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
# from services.auth_service import AuthService
from services.ocr_service import OCRService
from services.text_processing_service import TextProcessingService

# .env 로딩
load_dotenv()

# FastAPI 앱 생성
app = FastAPI()

# 서비스 인스턴스 생성
# auth_service = AuthService()
ocr_service = OCRService()
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



# 텍스트 처리용 모델
class TextRequest(BaseModel):
    text: str

# 텍스트 처리 API
@app.post("/keyword_parser")
def process_text(request: TextRequest):
    result = text_processor.process_text(request.text)
    return result

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