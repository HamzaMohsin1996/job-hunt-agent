from langgraph.graph import StateGraph, END
from graph.state import JobHuntState
from graph.nodes import cover_node, networking_node, review_node


def build_graph():
    graph = StateGraph(JobHuntState)

    graph.add_node("cover", cover_node)
    graph.add_node("networking", networking_node)
    graph.add_node("review", review_node)

    graph.set_entry_point("cover")

    graph.add_conditional_edges(
        "cover",
        lambda state: state.task,
        {
            "cover": END,
            "networking": "networking",
            "review": "review",
        }
    )

    graph.add_edge("networking", END)
    graph.add_edge("review", END)

    return graph.compile()
