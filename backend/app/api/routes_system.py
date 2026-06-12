from fastapi import APIRouter
from app.core.config import settings


router = APIRouter(prefix="/system", tags=["System"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "llm_provider": settings.llm_provider,
        "chess_engine_provider": settings.chess_engine_provider,
        "database_provider": settings.database_provider,
    }