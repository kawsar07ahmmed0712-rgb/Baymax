import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.live_game_service import LiveGameManager


def main():
    print("Starting Baymax SQLite persistence smoke test...")

    manager_1 = LiveGameManager()

    game = manager_1.create_game(
        white_agent_id="alpha_attacker",
        black_agent_id="shadow_defender",
        max_moves=20,
    )

    game_id = game["game_id"]
    print("Created game:")
    print(game_id)

    step = manager_1.play_one_step(game_id)

    assert step["ok"] is True
    assert len(step["game"]["state"]["move_history"]) == 1

    print("Move saved:")
    print(step["last_move"])

    # Simulate server restart by creating a new manager.
    manager_2 = LiveGameManager()

    loaded_game = manager_2.get_game(game_id)

    assert loaded_game["game_id"] == game_id
    assert len(loaded_game["state"]["move_history"]) == 1

    print("Loaded game from SQLite:")
    print(loaded_game["game_id"])
    print(loaded_game["state"]["move_history"])

    history = manager_2.list_games()
    assert len(history) > 0

    print("History preview:")
    print(history[:3])

    print("DB health:")
    print(manager_2.storage_health())

    print("Baymax SQLite persistence smoke test passed.")


if __name__ == "__main__":
    main()