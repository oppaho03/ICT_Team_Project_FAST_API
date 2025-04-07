from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from fastapi_app.services.pagint_health_info_service import fetch_disease_info

router = APIRouter()

@router.get("/disease-info")
def get_disease_info(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    category: str = Query(None)
):
    """
    ✅ Oracle DB에서 질병 정보 10개씩 꺼내주는 API
    - page: 1페이지부터 시작
    - size: 한 페이지당 항목 수
    - category: 필터용 (예: 암, 고혈압 등)
    """
    result = fetch_disease_info(page, size, category)
    return JSONResponse(content=result)
