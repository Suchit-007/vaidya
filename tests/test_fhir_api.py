import pytest
from fastapi.testclient import TestClient
from startup_pro.backend.main import app

def test_export_fhir_endpoint():
    client = TestClient(app)
    analysis_data = {
        "answer": "Haridra helps in wound healing.",
        "confidence_tier": "HIGH",
        "extracted_entities": []
    }
    
    response = client.post("/api/export-fhir", json=analysis_data)
    assert response.status_code == 200
    bundle = response.json()
    assert bundle["resourceType"] == "Bundle"
