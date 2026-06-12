from app.agents.base_agent import ChessAgent
from app.agents.personalities import get_default_agent


def create_agent(agent_id: str) -> ChessAgent:
    config = get_default_agent(agent_id)
    return ChessAgent(config)