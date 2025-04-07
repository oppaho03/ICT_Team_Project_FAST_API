from fastapi import APIRouter
from pydantic import BaseModel
from fastapi_app.services.text_processing_service import TextProcessingService

router = APIRouter()
text_processor = TextProcessingService()

class TextRequest(BaseModel):
    text: str

@router.post("/keyword_parser")
def process_text(request: TextRequest):
    result = text_processor.process_text(request.text)
    return result
