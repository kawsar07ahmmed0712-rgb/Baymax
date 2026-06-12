from fastapi import APIRouter

from app.adapters.llm.provider_factory import get_llm_provider
from app.core.config import settings


router = APIRouter(prefix="/system", tags=["System"])


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "llm_provider": settings.llm_provider,
        "llm_model": settings.ollama_model,
        "chess_engine_provider": settings.chess_engine_provider,
        "database_provider": settings.database_provider,
    }


@router.get("/llm-health")
def llm_health_check():
    llm = get_llm_provider()
    return llm.health_check()