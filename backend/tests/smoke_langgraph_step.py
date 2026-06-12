import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.live_game_service import live_game_manager


def main():
    print("Starting Baymax LangGraph one-move smoke test...")

    game = live_game_manager.create_game(
        white_agent_id="alpha_attacker",
        black_agent_id="shadow_defender",
        max_moves=20,
    )

    game_id = game["game_id"]

    print("Created game:")
    print(game_id)

    step_1 = live_game_manager.play_one_step(game_id)
    print("Step 1:")
    print(step_1["last_move"])

    assert step_1["ok"] is True
    assert step_1["workflow"] == "langgraph_one_move"
    assert len(step_1["game"]["state"]["move_history"]) == 1

    step_2 = live_game_manager.play_one_step(game_id)
    print("Step 2:")
    print(step_2["last_move"])

    assert step_2["ok"] is True
    assert step_2["workflow"] == "langgraph_one_move"
    assert len(step_2["game"]["state"]["move_history"]) == 2

    print("Current FEN:")
    print(step_2["game"]["state"]["fen"])

    print("Baymax LangGraph one-move smoke test passed.")


if __name__ == "__main__":
    main()