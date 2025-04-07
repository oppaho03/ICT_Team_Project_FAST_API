from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi_app.services.text_processing_service import TextProcessingService
from fastapi_app.services.db_service import save_text_processing_result

router = APIRouter()
text_processor = TextProcessingService()

class TextRequest(BaseModel):
    text: str

@router.post("/keyword_parser")
def process_text(request: TextRequest):
    # 🔹 1. 텍스트 처리
    result = text_processor.process_text(request.text)

    # 🔹 2. DB 저장
    try:
        save_text_processing_result(
            original_text=result["original_text"],
            processed_text=result["processed_text"],
            keywords=result["keywords"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB 저장 실패: {str(e)}")

    # 🔹 3. 결과 반환
    return result
