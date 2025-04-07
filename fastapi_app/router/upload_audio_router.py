# fastapi_app/router/upload_audio_router.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi_app.services.audio_service import analyze_audio_and_generate_result
from fastapi_app.services.result_sender import send_results_to_springboot

router = APIRouter()
UPLOAD_FOLDER = "./audio_data"

@router.post("/analyze_and_send")
async def analyze_audio_and_send(file: UploadFile = File(...)):
    """🎧 오디오 파일 업로드 → 분석 → 결과를 SpringBoot로 전송"""
    try:
        result = analyze_audio_and_generate_result(file, UPLOAD_FOLDER)
        send_results_to_springboot(result)
        return JSONResponse(content={"message": "분석 완료 및 스프링 서버 전송 완료 ✅"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 분석 중 오류 발생: {str(e)}")
