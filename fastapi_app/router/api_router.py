from fastapi import APIRouter
from fastapi_app.router.upload_audio_router import router as stt_router
from fastapi_app.router.ocr_router import router as ocr_router
from fastapi_app.router.text_processing_router import router as text_router
from fastapi_app.router.paging_health_information import router as health_router

router = APIRouter()

router.include_router(stt_router, prefix="/audio")
router.include_router(ocr_router, prefix="/ocr")
router.include_router(text_router, prefix="/keyword")
router.include_router(health_router, prefix="/health")
