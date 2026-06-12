import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.chess.board_manager import create_initial_state, apply_move, get_board_summary
from app.chess.move_validator import validate_move
from app.chess.pgn_exporter import export_moves_to_pgn

def main():
    print("Starting Baymax chess core smoke test...")

    state = create_initial_state()

    print("Initial FEN:")
    print(state["fen"])

    assert state["turn"] == "white"
    assert "e2e4" in state["legal_moves"]

    valid = validate_move(state["fen"], "e2e4")
    assert valid["is_legal"] is True

    invalid = validate_move(state["fen"], "e2e5")
    assert invalid["is_legal"] is False

    state = apply_move(state["fen"], "e2e4", state["move_history"])
    assert state["ok"] is True
    assert state["turn"] == "black"

    state = apply_move(state["fen"], "e7e5", state["move_history"])
    assert state["ok"] is True
    assert state["turn"] == "white"

    state = apply_move(state["fen"], "g1f3", state["move_history"])
    assert state["ok"] is True

    summary = get_board_summary(state["fen"])
    print("Current board summary:")
    print(summary)

    pgn = export_moves_to_pgn(state["move_history"])
    print("Generated PGN:")
    print(pgn)

    print("Baymax chess core smoke test passed.")


if __name__ == "__main__":
    main()