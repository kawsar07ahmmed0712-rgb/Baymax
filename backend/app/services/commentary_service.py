from app.adapters.llm.provider_factory import get_llm_provider


def build_fallback_commentary(
    agent_name: str,
    move_san: str,
    move_uci: str,
    agent_style: str,
) -> str:
    return (
        f"{agent_name} played {move_san} ({move_uci}). "
        f"This was selected by the engine-guided {agent_style} agent."
    )


def generate_move_commentary(
    agent: dict,
    decision: dict,
    last_move: dict,
    previous_fen: str,
    new_fen: str,
) -> dict:
    """
    Generate short AI commentary for one chess move.

    If Ollama is unavailable, return fallback commentary.
    """
    agent_name = agent.get("name", "Baymax Agent")
    agent_style = agent.get("style", "balanced")
    move_uci = last_move.get("uci", "")
    move_san = last_move.get("san", move_uci)

    candidates = decision.get("candidates", [])
    candidate_text = "\n".join(
        [
            f"- {item.get('san', item.get('move'))} ({item.get('move')}), score={item.get('score')}"
            for item in candidates[:3]
        ]
    )

    system_prompt = (
        "You are Baymax, a helpful chess commentary assistant. "
        "Explain chess moves simply and briefly. "
        "Do not hallucinate. "
        "Keep the answer under 45 words."
    )

    prompt = f"""
Agent: {agent_name}
Agent style: {agent_style}

Move played:
{move_san} ({move_uci})

Previous FEN:
{previous_fen}

New FEN:
{new_fen}

Top engine candidates:
{candidate_text}

Write a short chess commentary explaining why this move makes sense.
"""

    fallback = build_fallback_commentary(
        agent_name=agent_name,
        move_san=move_san,
        move_uci=move_uci,
        agent_style=agent_style,
    )

    try:
        llm = get_llm_provider()
        response = llm.generate(prompt=prompt, system_prompt=system_prompt)

        if not response["ok"] or not response.get("text"):
            return {
                "ok": False,
                "provider": response.get("provider"),
                "model": response.get("model"),
                "text": fallback,
                "fallback": True,
                "error": response.get("error", "LLM failed"),
            }

        return {
            "ok": True,
            "provider": response.get("provider"),
            "model": response.get("model"),
            "text": response["text"],
            "fallback": False,
        }

    except Exception as exc:
        return {
            "ok": False,
            "provider": None,
            "model": None,
            "text": fallback,
            "fallback": True,
            "error": str(exc),
        }