from fastapi import APIRouter, UploadFile, File
from fastapi_app.services.ocr_service import OCRService
from fastapi_app.services.openai_service import OpenAIService
from fastapi_app.services.text_processing_service import TextProcessingService

router = APIRouter()
ocr_service = OCRService()
openai_service = OpenAIService()
text_processor = TextProcessingService()

@router.post("/upload")
async def ocr_test(file: UploadFile = File(...)):
    """
    ✅ 단순 파일 업로드 확인
    """
    contents = await file.read()
    return {
        "filename": file.filename,
        "filesize": len(contents)
    }

@router.post("/analyze")
async def ocr_and_analyze(file: UploadFile = File(...)):
    """
    ✅ OCR 수행 후 GPT로 질병 예측
    """
    image_bytes = await file.read()
    ocr_result = ocr_service.run_ocr(image_bytes)
    ocr_text = "\n".join(ocr_result)
    gpt_response = openai_service.ask_about_prescription(ocr_text)

    return {
        "ocr_raw": ocr_text,
        "gpt_analysis": gpt_response
    }

@router.post("/analyze_with_keywords")
async def full_ocr_pipeline(file: UploadFile = File(...)):
    """
    ✅ OCR → GPT 분석 → 키워드 분류까지 한 번에 수행하는 API
    """
    image_bytes = await file.read()
    ocr_result = ocr_service.run_ocr(image_bytes)
    ocr_text = "\n".join(ocr_result)

    gpt_response = openai_service.ask_about_prescription(ocr_text)
    keyword_result = text_processor.process_text(gpt_response)

    return {
        "ocr_raw": ocr_text,
        "gpt_analysis": gpt_response,
        "keyword_analysis": keyword_result
    }
