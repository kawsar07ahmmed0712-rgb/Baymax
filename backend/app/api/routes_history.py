from fastapi import APIRouter

from app.services.live_game_service import live_game_manager


router = APIRouter(prefix="/history", tags=["History"])


@router.get("")
def get_history():
    return {
        "ok": True,
        "games": live_game_manager.list_games(),
    }