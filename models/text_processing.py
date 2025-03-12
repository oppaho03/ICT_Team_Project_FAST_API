from pydantic import BaseModel
from typing import List

class TextProcessingRequest(BaseModel):
    text: str

class TextProcessingResponse(BaseModel):
    original_text: str
    processed_text: str
    keywords: List[str]


# 데이터베이스 얘기 후 필요 컬럼 추가
# 여기 추가하면 services_db에도 추가해야함 (인자)