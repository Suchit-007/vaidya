import pytest
from startup_pro.backend.agents.graph import debate_app
from langchain_core.messages import HumanMessage

@pytest.mark.asyncio
async def test_graph_execution():
    initial_state = {
        "messages": [HumanMessage(content="What are the benefits of Haridra?")],
        "consensus_reached": False,
        "safety_check_passed": False,
        "trace": []
    }
    
    # Run the graph
    result = await debate_app.ainvoke(initial_state)
    
    assert "messages" in result
    assert len(result["trace"]) > 0
    # Check if at least one agent node was visited
    agents_visited = [t["agent"] for t in result["trace"]]
    assert "Scholar" in agents_visited or "Pharmacologist" in agents_visited or "SafetyOfficer" in agents_visited
