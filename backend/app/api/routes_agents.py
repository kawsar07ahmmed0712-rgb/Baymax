from fastapi import APIRouter

from app.agents.personalities import list_default_agents


router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("")
def get_agents():
    return {
        "ok": True,
        "agents": list_default_agents(),
    }