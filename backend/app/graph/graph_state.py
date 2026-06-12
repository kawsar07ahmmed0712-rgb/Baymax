from typing import Any, TypedDict


class MoveGraphState(TypedDict, total=False):
    """
    Shared state for one AI chess move workflow.
    """

    game: dict[str, Any]
    board_state: dict[str, Any]

    ok: bool
    reason: str | None

    current_turn: str
    agent_id: str
    agent: dict[str, Any]
    agent_object: Any

    decision: dict[str, Any]
    updated_state: dict[str, Any]
    last_move: dict[str, Any]

    result: dict[str, Any]