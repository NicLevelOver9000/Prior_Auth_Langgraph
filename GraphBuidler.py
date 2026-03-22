from langgraph.graph import StateGraph, END

from nodes.Form_node import form_node
from nodes.Labs_node import labs_node
from nodes.Imaging_node import imaging_node
from nodes.Notes_node import notes_node
from nodes.Orchestrator_node import orchestrator_node
from State import PriorAuthState

# ----------------------------
# Build Graph
# ----------------------------


def build_graph():

    workflow = StateGraph(PriorAuthState)

    # Add nodes
    workflow.add_node("form", form_node)
    workflow.add_node("labs", labs_node)
    workflow.add_node("imaging", imaging_node)
    workflow.add_node("notes", notes_node)
    workflow.add_node("orchestrator", orchestrator_node)

    # Entry point
    workflow.set_entry_point("form")

    # Flow
    workflow.add_edge("form", "labs")
    workflow.add_edge("labs", "imaging")
    workflow.add_edge("imaging", "notes")
    workflow.add_edge("notes", "orchestrator")

    workflow.add_edge("orchestrator", END)

    return workflow.compile()
