import pytest
from startup_pro.backend.rag_engine import RagEngine

def test_rag_seasonal_reweighting():
    engine = RagEngine(data_path="startup_pro/data")
    query = "Joint pain management"
    
    # Test for winter (Vata aggravating)
    results_winter = engine.query(query, month=1)
    # Test for summer (Pitta aggravating)
    results_summer = engine.query(query, month=5)
    
    # Check if the seasonal ritu is mentioned in metadata or results
    assert "ritu" in results_winter
    assert results_winter["ritu"] == "Sisira"
    assert results_summer["ritu"] == "Grishma"
