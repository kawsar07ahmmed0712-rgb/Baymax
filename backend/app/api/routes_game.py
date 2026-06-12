from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.live_game_service import live_game_manager


router = APIRouter(prefix="/game", tags=["Game"])


class CreateGameRequest(BaseModel):
    white_agent_id: str = Field(default="alpha_attacker")
    black_agent_id: str = Field(default="shadow_defender")
    max_moves: int = Field(default=300, ge=1, le=500)


@router.post("/new")
def create_game(payload: CreateGameRequest):
    try:
        game = live_game_manager.create_game(
            white_agent_id=payload.white_agent_id,
            black_agent_id=payload.black_agent_id,
            max_moves=payload.max_moves,
        )

        return {
            "ok": True,
            "message": "Game created",
            "game": game,
        }

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/list")
def list_games():
    return {
        "ok": True,
        "games": live_game_manager.list_games(),
    }


@router.get("/{game_id}")
def get_game(game_id: str):
    try:
        game = live_game_manager.get_game(game_id)

        return {
            "ok": True,
            "game": game,
        }

    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{game_id}/step")
def play_one_step(game_id: str):
    try:
        result = live_game_manager.play_one_step(game_id)
        return result

    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/{game_id}/reset")
def reset_game(game_id: str):
    try:
        game = live_game_manager.reset_game(game_id)

        return {
            "ok": True,
            "message": "Game reset",
            "game": game,
        }

    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{game_id}/pgn")
def export_pgn(game_id: str):
    try:
        pgn = live_game_manager.export_game_pgn(game_id)

        return {
            "ok": True,
            "game_id": game_id,
            "pgn": pgn,
        }

    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc