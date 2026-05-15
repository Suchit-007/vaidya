import requests
import json

def test_roadmap():
    url = "http://localhost:8000/api/roadmap"
    payload = {
        "disease": "Joint Pain",
        "dosha": "Vata",
        "age": "Adult",
        "severity": "Moderate"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            # print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_roadmap()
