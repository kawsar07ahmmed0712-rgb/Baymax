from app.adapters.database.base import BaseGameStore


class PostgresGameStore(BaseGameStore):
    """
    Placeholder for future cloud deployment.

    Later:
    - PostgreSQL
    - Supabase
    - Railway/Render DB
    """

    def health_check(self) -> dict:
        return {
            "ok": False,
            "provider": "postgres",
            "reason": "PostgreSQL provider is not implemented yet.",
        }

    def save_game(self, game: dict) -> dict:
        return {
            "ok": False,
            "provider": "postgres",
            "error": "PostgreSQL provider is not implemented yet.",
        }

    def get_game(self, game_id: str) -> dict | None:
        return None

    def list_games(self, limit: int = 50) -> list[dict]:
        return []