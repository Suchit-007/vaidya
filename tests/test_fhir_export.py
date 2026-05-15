import pytest
from startup_pro.backend.fhir import generate_fhir_bundle

def test_fhir_bundle_generation():
    analysis_data = {
        "answer": "Haridra helps in wound healing.",
        "confidence_tier": "HIGH",
        "source_text": "Charaka Samhita",
        "extracted_entities": [
            {"term": "Haridra", "definition": "Turmeric"}
        ]
    }
    
    bundle = generate_fhir_bundle(analysis_data)
    
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert len(bundle["entry"]) > 0
    
    # Check for Composition resource
    composition = next(e["resource"] for e in bundle["entry"] if e["resource"]["resourceType"] == "Composition")
    assert composition["status"] == "final"
    assert "Haridra" in composition["section"][0]["text"]["div"]
