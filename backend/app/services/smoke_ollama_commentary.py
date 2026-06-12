import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.adapters.llm.provider_factory import get_llm_provider
from app.services.live_game_service import live_game_manager


def main():
    print("Starting Baymax Ollama commentary smoke test...")

    llm = get_llm_provider()
    health = llm.health_check()

    print("LLM health:")
    print(health)

    game = live_game_manager.create_game(
        white_agent_id="alpha_attacker",
        black_agent_id="shadow_defender",
        max_moves=20,
    )

    game_id = game["game_id"]

    step = live_game_manager.play_one_step(game_id)

    print("Last move:")
    print(step["last_move"])

    print("Commentary:")
    print(step.get("commentary"))

    assert step["ok"] is True
    assert "commentary" in step
    assert step["commentary"]["text"]

    print("Baymax Ollama commentary smoke test passed.")


if __name__ == "__main__":
    main()