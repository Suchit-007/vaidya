from datetime import datetime
from typing import Dict, Any, List

RITU_MAP = {
    "Sisira": {"months": [1, 2], "name": "Late Winter", "aggravated_doshas": ["Vata"], "dietary_preference": "Warm, Unctuous"},
    "Vasanta": {"months": [3, 4], "name": "Spring", "aggravated_doshas": ["Kapha"], "dietary_preference": "Light, Warm"},
    "Grishma": {"months": [5, 6], "name": "Summer", "aggravated_doshas": ["Pitta"], "dietary_preference": "Cool, Liquid"},
    "Varsha": {"months": [7, 8], "name": "Monsoon", "aggravated_doshas": ["Vata"], "dietary_preference": "Warm, Unctuous"},
    "Sharad": {"months": [9, 10], "name": "Autumn", "aggravated_doshas": ["Pitta"], "dietary_preference": "Sweet, Bitter, Cool"},
    "Hemanta": {"months": [11, 12], "name": "Early Winter", "aggravated_doshas": ["Kapha"], "dietary_preference": "Warm, Nourishing"}
}

def get_current_ritu(month: int = None, day: int = None) -> str:
    """Detects current Ayurvedic season (Ritu) based on Gregorian month."""
    if month is None:
        month = datetime.now().month
    
    for ritu, data in RITU_MAP.items():
        if month in data["months"]:
            return ritu
    return "Sisira" # Fallback

def get_ritu_adjustments(ritu: str) -> Dict[str, Any]:
    """Returns clinical adjustments for a given Ritu."""
    return RITU_MAP.get(ritu, RITU_MAP["Sisira"])
