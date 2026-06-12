import chess

from app.chess.move_validator import (
    create_board_from_fen,
    get_legal_moves,
    validate_move,
)
from app.chess.game_result import get_game_status


def create_initial_state() -> dict:
    """
    Create a new chess game state.
    """
    board = chess.Board()

    return {
        "fen": board.fen(),
        "turn": "white",
        "move_number": board.fullmove_number,
        "legal_moves": get_legal_moves(board.fen()),
        "move_history": [],
        "game_status": get_game_status(board.fen()),
    }


def get_board_summary(fen: str) -> dict:
    """
    Return useful board information from FEN.
    """
    board = create_board_from_fen(fen)

    return {
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "move_number": board.fullmove_number,
        "legal_moves": get_legal_moves(board.fen()),
        "game_status": get_game_status(board.fen()),
    }


def apply_move(fen: str, move_uci: str, move_history: list[str] | None = None) -> dict:
    """
    Apply a legal UCI move to the board and return updated game state.
    """
    board = create_board_from_fen(fen)
    move_check = validate_move(fen, move_uci)

    if not move_check["is_legal"]:
        return {
            "ok": False,
            "error": move_check["reason"],
            "fen": fen,
            "move": move_uci,
        }

    move = chess.Move.from_uci(move_uci)
    san = board.san(move)
    board.push(move)

    updated_history = move_history[:] if move_history else []
    updated_history.append(move_uci)

    return {
        "ok": True,
        "fen": board.fen(),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "move_number": board.fullmove_number,
        "legal_moves": get_legal_moves(board.fen()),
        "move_history": updated_history,
        "last_move": {
            "uci": move_uci,
            "san": san,
        },
        "game_status": get_game_status(board.fen()),
    }


def reset_board() -> dict:
    """
    Reset game to the initial position.
    """
    return create_initial_state()