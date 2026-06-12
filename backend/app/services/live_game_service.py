from datetime import datetime, timezone

from app.adapters.database.db_factory import get_game_store
from app.agents.agent_factory import create_agent
from app.chess.board_manager import create_initial_state
from app.chess.pgn_exporter import export_moves_to_pgn
from app.core.config import settings
from app.graph.chess_graph import run_one_move_graph
from app.utils.ids import generate_id


class LiveGameManager:
    """
    Live game manager.

    It keeps active games in memory and also saves every game to SQLite.
    If a game is not found in memory, it tries to load it from SQLite.
    """

    def __init__(self):
        self.games: dict[str, dict] = {}
        self.store = get_game_store()

    def create_game(
        self,
        white_agent_id: str = "alpha_attacker",
        black_agent_id: str = "shadow_defender",
        max_moves: int | None = None,
    ) -> dict:
        white_agent = create_agent(white_agent_id)
        black_agent = create_agent(black_agent_id)

        game_id = generate_id("game")
        now = datetime.now(timezone.utc).isoformat()
        initial_state = create_initial_state()

        game = {
            "game_id": game_id,
            "created_at": now,
            "updated_at": now,
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
        self.store.save_game(game)

        return game

    def list_games(self) -> list[dict]:
        return self.store.list_games(limit=100)

    def get_game(self, game_id: str) -> dict:
        memory_game = self.games.get(game_id)

        if memory_game:
            return memory_game

        db_game = self.store.get_game(game_id)

        if db_game:
            self.games[game_id] = db_game
            return db_game

        raise KeyError(f"Game not found: {game_id}")

    def play_one_step(self, game_id: str) -> dict:
        """
        Play one move through LangGraph workflow and save updated state.
        """
        game = self.get_game(game_id)
        result = run_one_move_graph(game)

        if "game" in result:
            updated_game = result["game"]
            self.games[game_id] = updated_game
            self.store.save_game(updated_game)

        return result

    def reset_game(self, game_id: str) -> dict:
        game = self.get_game(game_id)

        game["state"] = create_initial_state()
        game["updated_at"] = datetime.now(timezone.utc).isoformat()

        self.games[game_id] = game
        self.store.save_game(game)

        return game

    def export_game_pgn(self, game_id: str) -> str:
        game = self.get_game(game_id)
        return export_moves_to_pgn(game["state"]["move_history"])

    def storage_health(self) -> dict:
        return self.store.health_check()


live_game_manager = LiveGameManager()