from app.adapters.engine.engine_factory import get_chess_engine


def check_engine_health() -> dict:
    """
    Check current chess engine status.
    """
    engine = get_chess_engine()
    return engine.health_check()


def get_engine_best_move(fen: str, depth: int | None = None) -> dict:
    """
    Get best move from selected engine.
    """
    engine = get_chess_engine()
    return engine.get_best_move(fen=fen, depth=depth)


def get_engine_top_moves(fen: str, depth: int | None = None, top_k: int | None = None) -> list[dict]:
    """
    Get top candidate moves from selected engine.
    """
    engine = get_chess_engine()
    return engine.get_top_moves(fen=fen, depth=depth, top_k=top_k)