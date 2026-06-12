from abc import ABC, abstractmethod


class BaseGameStore(ABC):
    """
    Base interface for game storage.

    Current:
    - SQLite local database

    Future:
    - PostgreSQL
    - Supabase
    - Cloud database
    """

    @abstractmethod
    def health_check(self) -> dict:
        pass

    @abstractmethod
    def save_game(self, game: dict) -> dict:
        pass

    @abstractmethod
    def get_game(self, game_id: str) -> dict | None:
        pass

    @abstractmethod
    def list_games(self, limit: int = 50) -> list[dict]:
        pass