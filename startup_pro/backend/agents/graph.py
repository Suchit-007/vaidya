from langgraph.graph import StateGraph, END
from startup_pro.backend.agents.state import AgentState
from startup_pro.backend.agents.nodes import scholar_node, pharmacologist_node, safety_officer_node

# Define the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("scholar", scholar_node)
workflow.add_node("pharmacologist", pharmacologist_node)
workflow.add_node("safety_officer", safety_officer_node)

# Add edges
workflow.set_entry_point("scholar")
workflow.add_edge("scholar", "pharmacologist")
workflow.add_edge("pharmacologist", "safety_officer")
workflow.add_edge("safety_officer", END)

# Compile the graph
debate_app = workflow.compile()
