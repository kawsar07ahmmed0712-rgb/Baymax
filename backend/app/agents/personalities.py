DEFAULT_AGENTS = {
    "alpha_attacker": {
        "id": "alpha_attacker",
        "name": "Alpha Attacker",
        "style": "aggressive",
        "description": "Prefers sharp tactical and attacking moves.",
        "risk_level": 0.85,
        "engine_depth": 6,
        "top_k": 3,
    },
    "shadow_defender": {
        "id": "shadow_defender",
        "name": "Shadow Defender",
        "style": "defensive",
        "description": "Prefers solid, safe, and defensive moves.",
        "risk_level": 0.25,
        "engine_depth": 6,
        "top_k": 3,
    },
    "balanced_master": {
        "id": "balanced_master",
        "name": "Balanced Master",
        "style": "balanced",
        "description": "Balances attack, defense, and positional play.",
        "risk_level": 0.50,
        "engine_depth": 6,
        "top_k": 3,
    },
}


def get_default_agent(agent_id: str) -> dict:
    agent = DEFAULT_AGENTS.get(agent_id)

    if not agent:
        raise ValueError(f"Unknown agent id: {agent_id}")

    return agent.copy()


def list_default_agents() -> list[dict]:
    return [agent.copy() for agent in DEFAULT_AGENTS.values()]