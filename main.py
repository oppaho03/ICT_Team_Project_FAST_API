from fastapi import FastAPI
from pydantic import BaseModel
from services.text_processing_service import TextProcessingService

# FastAPI 앱 생성
app = FastAPI()

# 텍스트 처리 서비스 인스턴스 생성
text_processor = TextProcessingService()

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
    return {"massage":"정상 작동중입니다 !! !! !!"}


# FastAPI 실행 (uvicorn 사용)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.65", port=8001)

# 서버 실행 방법
# uvicorn main:app --host 192.168.0.65 --port 8001 --reload