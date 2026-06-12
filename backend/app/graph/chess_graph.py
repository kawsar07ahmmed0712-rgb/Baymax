from langgraph.graph import END, START, StateGraph

from app.graph.graph_state import MoveGraphState
from app.graph.nodes import (
    apply_move_node,
    choose_agent_node,
    commentary_node,
    decide_move_node,
    finalize_step_node,
    load_game_node,
    route_after_decision,
    route_after_load,
)


def build_one_move_graph():
    """
    Build and compile one-move LangGraph workflow.
    """
    graph = StateGraph(MoveGraphState)

    graph.add_node("load_game", load_game_node)
    graph.add_node("choose_agent", choose_agent_node)
    graph.add_node("decide_move", decide_move_node)
    graph.add_node("apply_move", apply_move_node)
    graph.add_node("commentary", commentary_node)
    graph.add_node("finalize_step", finalize_step_node)

    graph.add_edge(START, "load_game")

    graph.add_conditional_edges(
        "load_game",
        route_after_load,
        {
            "continue": "choose_agent",
            "stop": END,
        },
    )

    graph.add_edge("choose_agent", "decide_move")

    graph.add_conditional_edges(
        "decide_move",
        route_after_decision,
        {
            "continue": "apply_move",
            "stop": END,
        },
    )

    graph.add_edge("apply_move", "commentary")
    graph.add_edge("commentary", "finalize_step")
    graph.add_edge("finalize_step", END)

    return graph.compile()


one_move_graph = build_one_move_graph()


def run_one_move_graph(game: dict) -> dict:
    """
    Run compiled LangGraph workflow for one chess move.
    """
    final_state = one_move_graph.invoke({"game": game})
    return final_state["result"]