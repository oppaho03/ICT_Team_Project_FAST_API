from fastapi import APIRouter, UploadFile, File
from fastapi_app.services.ocr_service import OCRService
from fastapi_app.services.openai_service import OpenAIService

router = APIRouter()
ocr_service = OCRService()
openai_service = OpenAIService()

@router.post("/upload")
async def ocr_test(file: UploadFile = File(...)):
    contents = await file.read()
    return {
        "filename": file.filename,
        "filesize": len(contents)
    }

@router.post("/analyze")
async def ocr_and_analyze(file: UploadFile = File(...)):
    image_bytes = await file.read()
    ocr_result = ocr_service.run_ocr_from_bytes(image_bytes)
    ocr_text = "\n".join(ocr_result)
    gpt_response = openai_service.ask_about_prescription(ocr_text)
    return {
        "ocr_raw": ocr_text,
        "gpt_analysis": gpt_response
    }
