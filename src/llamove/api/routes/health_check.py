from fastapi import APIRouter
from llamove import schemas

router = APIRouter()


@router.get("/health", response_model=schemas.HealthResponse)
async def health():
    return schemas.HealthResponse(status=True)
