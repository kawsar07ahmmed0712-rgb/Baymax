from app.adapters.engine.base import BaseChessEngine
from app.adapters.engine.stockfish_provider import StockfishProvider
from app.core.config import settings


def get_chess_engine() -> BaseChessEngine:
    """
    Return selected chess engine provider based on .env config.
    """
    provider = settings.chess_engine_provider.lower().strip()

    if provider == "stockfish":
        return StockfishProvider()

    raise ValueError(f"Unsupported chess engine provider: {settings.chess_engine_provider}")