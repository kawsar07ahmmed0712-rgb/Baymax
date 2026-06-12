import chess


def create_board_from_fen(fen: str | None = None) -> chess.Board:
    """
    Create a chess board from FEN.
    If FEN is None, create a new starting board.
    """
    try:
        if fen:
            return chess.Board(fen)
        return chess.Board()
    except ValueError as exc:
        raise ValueError(f"Invalid FEN: {fen}") from exc


def get_legal_moves(fen: str | None = None) -> list[str]:
    """
    Return all legal moves in UCI format.
    Example: e2e4, g1f3, e7e8q
    """
    board = create_board_from_fen(fen)
    return [move.uci() for move in board.legal_moves]


def validate_move(fen: str, move_uci: str) -> dict:
    """
    Validate whether a UCI move is legal in the given board position.
    """
    board = create_board_from_fen(fen)

    try:
        move = chess.Move.from_uci(move_uci)
    except ValueError:
        return {
            "is_legal": False,
            "move": move_uci,
            "reason": "Invalid UCI move format",
        }

    if move not in board.legal_moves:
        return {
            "is_legal": False,
            "move": move_uci,
            "reason": "Move is not legal in this position",
        }

    return {
        "is_legal": True,
        "move": move_uci,
        "reason": "Legal move",
        "san": board.san(move),
    }


def get_turn_from_fen(fen: str) -> str:
    """
    Return whose turn it is.
    """
    board = create_board_from_fen(fen)
    return "white" if board.turn == chess.WHITE else "black"