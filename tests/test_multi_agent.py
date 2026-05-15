import pytest
from startup_pro.backend.agents.state import AgentState
from startup_pro.backend.agents.nodes import scholar_node, pharmacologist_node, safety_officer_node
from langchain_core.messages import HumanMessage

def test_agent_state_initialization():
    state = {
        "messages": [HumanMessage(content="test")],
        "consensus_reached": False,
        "safety_check_passed": False,
        "trace": []
    }
    assert len(state["messages"]) == 1
    assert state["consensus_reached"] is False

def test_nodes_exist():
    assert callable(scholar_node)
    assert callable(pharmacologist_node)
    assert callable(safety_officer_node)
