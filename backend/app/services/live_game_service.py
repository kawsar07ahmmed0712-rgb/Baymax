from datetime import datetime, timezone

from app.agents.agent_factory import create_agent
from app.chess.board_manager import create_initial_state, apply_move
from app.chess.pgn_exporter import export_moves_to_pgn
from app.core.config import settings
from app.utils.ids import generate_id


class LiveGameManager:
    """
    In-memory live game manager.

    This is for MVP API testing.
    Later, this will be replaced/extended with SQLite/PostgreSQL.
    """

    def __init__(self):
        self.games: dict[str, dict] = {}

    def create_game(
        self,
        white_agent_id: str = "alpha_attacker",
        black_agent_id: str = "shadow_defender",
        max_moves: int | None = None,
    ) -> dict:
        white_agent = create_agent(white_agent_id)
        black_agent = create_agent(black_agent_id)

        game_id = generate_id("game")
        initial_state = create_initial_state()

        game = {
            "game_id": game_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "white_agent": {
                "id": white_agent.id,
                "name": white_agent.name,
                "style": white_agent.style,
            },
            "black_agent": {
                "id": black_agent.id,
                "name": black_agent.name,
                "style": black_agent.style,
            },
            "white_agent_id": white_agent_id,
            "black_agent_id": black_agent_id,
            "max_moves": max_moves or settings.max_game_moves,
            "state": initial_state,
        }

        self.games[game_id] = game
        return game

    def list_games(self) -> list[dict]:
        return [
            {
                "game_id": game["game_id"],
                "created_at": game["created_at"],
                "updated_at": game["updated_at"],
                "white_agent": game["white_agent"],
                "black_agent": game["black_agent"],
                "turn": game["state"]["turn"],
                "move_count": len(game["state"]["move_history"]),
                "game_status": game["state"]["game_status"],
            }
            for game in self.games.values()
        ]

    def get_game(self, game_id: str) -> dict:
        game = self.games.get(game_id)

        if not game:
            raise KeyError(f"Game not found: {game_id}")

        return game

    def _current_agent(self, game: dict):
        if game["state"]["turn"] == "white":
            return create_agent(game["white_agent_id"])

        return create_agent(game["black_agent_id"])

    def play_one_step(self, game_id: str) -> dict:
        game = self.get_game(game_id)
        state = game["state"]

        if state["game_status"]["game_over"]:
            return {
                "ok": False,
                "reason": "Game is already over",
                "game": game,
            }

        if len(state["move_history"]) >= game["max_moves"]:
            state["game_status"] = {
                "game_over": True,
                "result": "1/2-1/2",
                "reason": "max_move_limit_reached",
                "is_check": False,
                "turn": state["turn"],
            }

            game["updated_at"] = datetime.now(timezone.utc).isoformat()
            return {
                "ok": False,
                "reason": "max_move_limit_reached",
                "game": game,
            }

        agent = self._current_agent(game)
        decision = agent.choose_move(state["fen"])

        if not decision["ok"]:
            state["game_status"] = {
                "game_over": True,
                "result": "1/2-1/2",
                "reason": decision.get("reason", "agent_failed"),
                "is_check": False,
                "turn": state["turn"],
            }

            game["updated_at"] = datetime.now(timezone.utc).isoformat()
            return {
                "ok": False,
                "reason": decision.get("reason", "agent_failed"),
                "decision": decision,
                "game": game,
            }

        updated_state = apply_move(
            fen=state["fen"],
            move_uci=decision["selected_move"],
            move_history=state["move_history"],
        )

        if not updated_state["ok"]:
            state["game_status"] = {
                "game_over": True,
                "result": "1/2-1/2",
                "reason": updated_state.get("error", "illegal_move"),
                "is_check": False,
                "turn": state["turn"],
            }

            game["updated_at"] = datetime.now(timezone.utc).isoformat()
            return {
                "ok": False,
                "reason": updated_state.get("error", "illegal_move"),
                "decision": decision,
                "game": game,
            }

        game["state"] = updated_state
        game["updated_at"] = datetime.now(timezone.utc).isoformat()

        return {
            "ok": True,
            "agent": {
                "id": agent.id,
                "name": agent.name,
                "style": agent.style,
            },
            "decision": decision,
            "last_move": updated_state["last_move"],
            "game": game,
        }

    def reset_game(self, game_id: str) -> dict:
        game = self.get_game(game_id)
        game["state"] = create_initial_state()
        game["updated_at"] = datetime.now(timezone.utc).isoformat()
        return game

    def export_game_pgn(self, game_id: str) -> str:
        game = self.get_game(game_id)
        return export_moves_to_pgn(game["state"]["move_history"])


live_game_manager = LiveGameManager()