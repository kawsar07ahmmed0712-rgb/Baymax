from datetime import datetime
from pathlib import Path

from app.agents.agent_factory import create_agent
from app.chess.board_manager import create_initial_state, apply_move
from app.chess.pgn_exporter import export_moves_to_pgn
from app.core.config import settings


class TerminalAIMatch:
    """
    Runs a complete AI-vs-AI chess match in terminal.
    """

    def __init__(
        self,
        white_agent_id: str = "alpha_attacker",
        black_agent_id: str = "shadow_defender",
        max_moves: int | None = None,
    ):
        self.white_agent = create_agent(white_agent_id)
        self.black_agent = create_agent(black_agent_id)
        self.max_moves = max_moves or settings.max_game_moves
        self.state = create_initial_state()

    def _current_agent(self):
        return self.white_agent if self.state["turn"] == "white" else self.black_agent

    def play_one_move(self) -> dict:
        agent = self._current_agent()

        decision = agent.choose_move(self.state["fen"])

        if not decision["ok"]:
            self.state["game_status"] = {
                "game_over": True,
                "result": "1/2-1/2",
                "reason": decision.get("reason", "agent_failed"),
            }
            return {
                "ok": False,
                "reason": decision.get("reason", "agent_failed"),
                "state": self.state,
            }

        move_uci = decision["selected_move"]

        updated = apply_move(
            fen=self.state["fen"],
            move_uci=move_uci,
            move_history=self.state["move_history"],
        )

        if not updated["ok"]:
            self.state["game_status"] = {
                "game_over": True,
                "result": "1/2-1/2",
                "reason": updated.get("error", "illegal_move"),
            }
            return {
                "ok": False,
                "reason": updated.get("error", "illegal_move"),
                "decision": decision,
                "state": self.state,
            }

        self.state = updated

        return {
            "ok": True,
            "agent": {
                "id": agent.id,
                "name": agent.name,
                "style": agent.style,
            },
            "decision": decision,
            "last_move": updated["last_move"],
            "state": self.state,
        }

    def play_full_game(self, verbose: bool = True) -> dict:
        if verbose:
            print("Baymax AI-vs-AI match started")
            print(f"White: {self.white_agent.name} ({self.white_agent.style})")
            print(f"Black: {self.black_agent.name} ({self.black_agent.style})")
            print("-" * 70)

        while not self.state["game_status"]["game_over"]:
            if len(self.state["move_history"]) >= self.max_moves:
                self.state["game_status"] = {
                    "game_over": True,
                    "result": "1/2-1/2",
                    "reason": "max_move_limit_reached",
                    "is_check": False,
                    "turn": self.state["turn"],
                }
                break

            step = self.play_one_move()

            if verbose:
                move_no = len(self.state["move_history"])
                agent_name = step.get("agent", {}).get("name", "Unknown Agent")
                last_move = step.get("last_move", {})
                uci = last_move.get("uci")
                san = last_move.get("san")
                print(f"{move_no:03d}. {agent_name}: {san} ({uci})")

            if not step["ok"]:
                break

        pgn = export_moves_to_pgn(self.state["move_history"])

        if verbose:
            print("-" * 70)
            print("Game finished")
            print(f"Result: {self.state['game_status']['result']}")
            print(f"Reason: {self.state['game_status']['reason']}")
            print(f"Total half-moves: {len(self.state['move_history'])}")

        return {
            "white_agent": {
                "id": self.white_agent.id,
                "name": self.white_agent.name,
                "style": self.white_agent.style,
            },
            "black_agent": {
                "id": self.black_agent.id,
                "name": self.black_agent.name,
                "style": self.black_agent.style,
            },
            "final_state": self.state,
            "pgn": pgn,
        }


def save_match_pgn(pgn: str, output_dir: str = "../data/exports") -> str:
    """
    Save PGN to data/exports.
    """
    export_dir = Path(output_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = export_dir / f"baymax_match_{timestamp}.pgn"

    path.write_text(pgn, encoding="utf-8")

    return str(path)