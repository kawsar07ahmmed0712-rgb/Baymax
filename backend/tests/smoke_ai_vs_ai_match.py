import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.game_service import TerminalAIMatch, save_match_pgn


def main():
    print("Starting Baymax AI-vs-AI terminal match smoke test...")

    match = TerminalAIMatch(
        white_agent_id="alpha_attacker",
        black_agent_id="shadow_defender",
        max_moves=40,
    )

    result = match.play_full_game(verbose=True)

    assert "final_state" in result
    assert "pgn" in result
    assert len(result["final_state"]["move_history"]) > 0

    saved_path = save_match_pgn(result["pgn"])

    print("PGN saved to:")
    print(saved_path)

    print("Final FEN:")
    print(result["final_state"]["fen"])

    print("PGN preview:")
    print(result["pgn"][:800])

    print("Baymax AI-vs-AI terminal match smoke test passed.")


if __name__ == "__main__":
    main()