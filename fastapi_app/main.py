from dotenv import load_dotenv
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi_app.services import auth_service, ocr_service
from services.text_processing_service import TextProcessingService
import os

# FastAPI 앱 생성
app = FastAPI()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
# 텍스트 처리 서비스 인스턴스 생성
text_processor = TextProcessingService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 필요 시 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ocr
@app.post("/ocr")
async def ocr_endpoint(
    file: UploadFile = File(...),
    user_id: str = Depends(auth_service.get_current_user)
):
    result = ocr_service.run_ocr(file)
    return {
        "user_id": user_id,
        "result": result
    }


# 요청 바디 모델 정의
class TextRequest(BaseModel):
    text: str

@app.post("/keyword_parser")
def process_text(request: TextRequest):
    """
    입력된 텍스트를 변환 및 분석하여 반환하는 API
    """
    result = text_processor.process_text(request.text)
    return result

@app.get("/test")
def test_api():
    return {"message":"정상 작동중입니다 ! ! ! !"}

# FastAPI 실행 (uvicorn 사용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)



# 서버 실행 방법
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload