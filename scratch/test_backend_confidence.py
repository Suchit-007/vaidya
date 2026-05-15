import requests
import json

BASE_URL = "http://localhost:8000"
__test__ = False

def run_query(query):
    print(f"\nTesting Query: {query}")
    try:
        response = requests.post(f"{BASE_URL}/api/query", json={"query": query})
        if response.status_code == 200:
            data = response.json()
            print(f"Confidence: {data['confidence_tier']}")
            print(f"Sources: {data.get('sources')}")
            print(f"Answer Sample: {data['answer'][:100]}...")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    run_query("What is Yogavahi?")
    run_query("Explain Anupana")
