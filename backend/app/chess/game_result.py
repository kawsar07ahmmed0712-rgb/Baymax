import chess

from app.chess.move_validator import create_board_from_fen


def get_game_status(fen: str) -> dict:
    """
    Check whether the game is ongoing, checkmate, stalemate, draw, etc.
    """
    board = create_board_from_fen(fen)

    status = {
        "game_over": board.is_game_over(claim_draw=True),
        "result": None,
        "reason": "ongoing",
        "is_check": board.is_check(),
        "turn": "white" if board.turn == chess.WHITE else "black",
    }

    if not status["game_over"]:
        return status

    status["result"] = board.result(claim_draw=True)

    if board.is_checkmate():
        status["reason"] = "checkmate"
    elif board.is_stalemate():
        status["reason"] = "stalemate"
    elif board.is_insufficient_material():
        status["reason"] = "insufficient_material"
    elif board.can_claim_threefold_repetition():
        status["reason"] = "threefold_repetition_claim"
    elif board.can_claim_fifty_moves():
        status["reason"] = "fifty_move_rule_claim"
    elif board.is_seventyfive_moves():
        status["reason"] = "seventyfive_move_rule"
    elif board.is_fivefold_repetition():
        status["reason"] = "fivefold_repetition"
    else:
        status["reason"] = "game_over"

    return status