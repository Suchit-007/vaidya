import pytest
from startup_pro.backend.ritu_engine import get_current_ritu, get_ritu_adjustments

def test_ritu_detection():
    # Test for various dates
    assert get_current_ritu(1, 15) == "Sisira" # Jan
    assert get_current_ritu(5, 15) == "Grishma" # May
    assert get_current_ritu(8, 15) == "Varsha" # Aug

def test_ritu_adjustments():
    adj = get_ritu_adjustments("Varsha")
    assert "Vata" in adj["aggravated_doshas"]
    assert adj["dietary_preference"] == "Warm, Unctuous"
