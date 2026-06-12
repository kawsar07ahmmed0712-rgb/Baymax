import chess
import chess.pgn
from io import StringIO


def export_moves_to_pgn(move_history: list[str]) -> str:
    """
    Convert UCI move history to PGN text.
    """
    board = chess.Board()
    game = chess.pgn.Game()
    game.headers["Event"] = "Baymax AI Chess Arena"
    game.headers["Site"] = "Local"
    game.headers["White"] = "Baymax White Agent"
    game.headers["Black"] = "Baymax Black Agent"

    node = game

    for move_uci in move_history:
        move = chess.Move.from_uci(move_uci)

        if move not in board.legal_moves:
            raise ValueError(f"Illegal move in history: {move_uci}")

        node = node.add_variation(move)
        board.push(move)

    game.headers["Result"] = board.result(claim_draw=True)

    output = StringIO()
    print(game, file=output, end="\n\n")
    return output.getvalue()