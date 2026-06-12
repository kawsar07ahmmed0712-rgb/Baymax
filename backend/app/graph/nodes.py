from datetime import datetime, timezone

from app.agents.agent_factory import create_agent
from app.chess.board_manager import apply_move
from app.graph.graph_state import MoveGraphState


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_game_node(state: MoveGraphState) -> MoveGraphState:
    """
    Load game and check if it can continue.
    """
    game = state["game"]
    board_state = game["state"]

    if board_state["game_status"]["game_over"]:
        return {
            "game": game,
            "board_state": board_state,
            "ok": False,
            "reason": "Game is already over",
            "result": {
                "ok": False,
                "reason": "Game is already over",
                "game": game,
            },
        }

    if len(board_state["move_history"]) >= game["max_moves"]:
        board_state["game_status"] = {
            "game_over": True,
            "result": "1/2-1/2",
            "reason": "max_move_limit_reached",
            "is_check": False,
            "turn": board_state["turn"],
        }

        game["state"] = board_state
        game["updated_at"] = _now_utc()

        return {
            "game": game,
            "board_state": board_state,
            "ok": False,
            "reason": "max_move_limit_reached",
            "result": {
                "ok": False,
                "reason": "max_move_limit_reached",
                "game": game,
            },
        }

    return {
        "game": game,
        "board_state": board_state,
        "ok": True,
        "reason": None,
        "current_turn": board_state["turn"],
    }


def choose_agent_node(state: MoveGraphState) -> MoveGraphState:
    """
    Select white or black agent based on board turn.
    """
    game = state["game"]
    current_turn = state["current_turn"]

    if current_turn == "white":
        agent_id = game["white_agent_id"]
    else:
        agent_id = game["black_agent_id"]

    agent_object = create_agent(agent_id)

    agent_info = {
        "id": agent_object.id,
        "name": agent_object.name,
        "style": agent_object.style,
    }

    return {
        **state,
        "agent_id": agent_id,
        "agent": agent_info,
        "agent_object": agent_object,
    }


def decide_move_node(state: MoveGraphState) -> MoveGraphState:
    """
    Ask selected agent to choose a move.
    """
    game = state["game"]
    board_state = state["board_state"]
    agent_object = state["agent_object"]

    decision = agent_object.choose_move(board_state["fen"])

    if not decision["ok"]:
        board_state["game_status"] = {
            "game_over": True,
            "result": "1/2-1/2",
            "reason": decision.get("reason", "agent_failed"),
            "is_check": False,
            "turn": board_state["turn"],
        }

        game["state"] = board_state
        game["updated_at"] = _now_utc()

        return {
            **state,
            "game": game,
            "board_state": board_state,
            "decision": decision,
            "ok": False,
            "reason": decision.get("reason", "agent_failed"),
            "result": {
                "ok": False,
                "reason": decision.get("reason", "agent_failed"),
                "decision": decision,
                "game": game,
            },
        }

    return {
        **state,
        "decision": decision,
        "ok": True,
        "reason": None,
    }


def apply_move_node(state: MoveGraphState) -> MoveGraphState:
    """
    Apply selected move to board.
    """
    game = state["game"]
    board_state = state["board_state"]
    decision = state["decision"]

    move_uci = decision["selected_move"]

    updated_state = apply_move(
        fen=board_state["fen"],
        move_uci=move_uci,
        move_history=board_state["move_history"],
    )

    if not updated_state["ok"]:
        board_state["game_status"] = {
            "game_over": True,
            "result": "1/2-1/2",
            "reason": updated_state.get("error", "illegal_move"),
            "is_check": False,
            "turn": board_state["turn"],
        }

        game["state"] = board_state
        game["updated_at"] = _now_utc()

        return {
            **state,
            "game": game,
            "board_state": board_state,
            "updated_state": updated_state,
            "ok": False,
            "reason": updated_state.get("error", "illegal_move"),
            "result": {
                "ok": False,
                "reason": updated_state.get("error", "illegal_move"),
                "decision": decision,
                "game": game,
            },
        }

    return {
        **state,
        "updated_state": updated_state,
        "last_move": updated_state["last_move"],
        "ok": True,
        "reason": None,
    }


def finalize_step_node(state: MoveGraphState) -> MoveGraphState:
    """
    Save updated board state back into game object and prepare API response.
    """
    game = state["game"]
    updated_state = state["updated_state"]

    game["state"] = updated_state
    game["updated_at"] = _now_utc()

    result = {
        "ok": True,
        "workflow": "langgraph_one_move",
        "agent": state["agent"],
        "decision": state["decision"],
        "last_move": state["last_move"],
        "game": game,
    }

    return {
        **state,
        "game": game,
        "result": result,
    }


def route_after_load(state: MoveGraphState) -> str:
    """
    Stop if game is over or max-move reached.
    """
    if state.get("ok") is False:
        return "stop"

    return "continue"


def route_after_decision(state: MoveGraphState) -> str:
    """
    Stop if agent failed to choose a move.
    """
    if state.get("ok") is False:
        return "stop"

    return "continue"