import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.chess.board_manager import create_initial_state, apply_move
from app.chess.engine_runner import (
    check_engine_health,
    get_engine_best_move,
    get_engine_top_moves,
)


def main():
    print("Starting Baymax Stockfish smoke test...")

    health = check_engine_health()
    print("Engine health:")
    print(health)

    state = create_initial_state()
    print("Initial FEN:")
    print(state["fen"])

    best = get_engine_best_move(state["fen"], depth=6)
    print("Best move:")
    print(best)

    assert best["ok"] is True
    assert best["best_move"] in state["legal_moves"]

    top_moves = get_engine_top_moves(state["fen"], depth=6, top_k=3)
    print("Top moves:")
    print(top_moves)

    assert len(top_moves) > 0

    state = apply_move(
        fen=state["fen"],
        move_uci=best["best_move"],
        move_history=state["move_history"],
    )

    assert state["ok"] is True

    print("State after Stockfish move:")
    print(state)

    print("Baymax Stockfish smoke test passed.")


if __name__ == "__main__":
    main()