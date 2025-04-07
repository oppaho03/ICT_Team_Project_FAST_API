from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_app.router import ocr_router
from fastapi_app.router.api_router import router as api_router

# .env 로딩
load_dotenv()

# FastAPI 앱 생성
app = FastAPI()

app.include_router(ocr_router.router)
# 라우터 등록
app.include_router(api_router)

# 서비스 인스턴스 생성
# (필요 시 라우터 내부에서 개별 인스턴스로 생성됨)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 도메인 지정 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
@app.get("/audio_test")
def read_root():
    return {"message": "음성 분석 API 서버가 실행 중입니다!"}

# 상태 확인 API
@app.get("/test")
def test_api():
    return {"message": "정상 작동중입니다 ! ! ! !"}

# FastAPI 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# FastAPI 실행
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="192.168.0.65", port=8001)


# 서버 실행 방법
# uvicorn main:app --host 192.168.0.65 --port 8001 --reload
# uvicorn fastapi_app.main:app --host 192.168.0.65 --port 8001 --reload
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
# uvicorn fastapi_app.main:app --host 127.0.0.1 --port 8001 --reload