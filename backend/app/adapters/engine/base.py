from abc import ABC, abstractmethod


class BaseChessEngine(ABC):
    """
    Base interface for chess engine providers.
    This allows us to use Stockfish now and replace it later if needed.
    """

    @abstractmethod
    def health_check(self) -> dict:
        pass

    @abstractmethod
    def get_best_move(self, fen: str, depth: int | None = None) -> dict:
        pass

    @abstractmethod
    def get_top_moves(self, fen: str, depth: int | None = None, top_k: int | None = None) -> list[dict]:
        pass