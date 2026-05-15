import pytest
from fastapi.testclient import TestClient
from startup_pro.backend.main import app

def test_websocket_trace_connection():
    client = TestClient(app)
    with client.websocket_connect("/ws/trace/test-query") as websocket:
        # Send a message to start the trace simulation
        websocket.send_json({"action": "start"})
        data = websocket.receive_json()
        assert "trace" in data
        assert data["trace"][0]["agent"] == "Scholar"
