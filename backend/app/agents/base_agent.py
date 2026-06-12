from app.chess.engine_runner import get_engine_best_move, get_engine_top_moves


class ChessAgent:
    """
    A simple chess agent.

    For now, this agent uses Stockfish candidate moves.
    Later, LangGraph + LLM will use these candidates and select moves with richer reasoning.
    """

    def __init__(self, config: dict):
        self.id = config["id"]
        self.name = config["name"]
        self.style = config["style"]
        self.description = config.get("description", "")
        self.risk_level = float(config.get("risk_level", 0.5))
        self.engine_depth = int(config.get("engine_depth", 6))
        self.top_k = int(config.get("top_k", 3))

    def choose_move(self, fen: str) -> dict:
        """
        Choose one move from the current position.

        Current rule:
        - aggressive: pick top Stockfish move
        - balanced: pick top Stockfish move
        - defensive: pick top Stockfish move

        Later:
        - use LLM/strategy to choose among top candidate moves
        """
        candidates = get_engine_top_moves(
            fen=fen,
            depth=self.engine_depth,
            top_k=self.top_k,
        )

        if candidates:
            selected = candidates[0]
            return {
                "ok": True,
                "agent_id": self.id,
                "agent_name": self.name,
                "agent_style": self.style,
                "selected_move": selected["move"],
                "selected_san": selected["san"],
                "candidates": candidates,
                "selection_reason": "Selected the strongest Stockfish candidate for this MVP step.",
            }

        best = get_engine_best_move(fen=fen, depth=self.engine_depth)

        if not best["ok"]:
            return {
                "ok": False,
                "agent_id": self.id,
                "agent_name": self.name,
                "reason": best.get("reason", "No move found"),
            }

        return {
            "ok": True,
            "agent_id": self.id,
            "agent_name": self.name,
            "agent_style": self.style,
            "selected_move": best["best_move"],
            "selected_san": None,
            "candidates": [best],
            "selection_reason": "Selected Stockfish best move.",
        }