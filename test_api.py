import requests
import json

url = "http://localhost:8000/triage"

payload = {
    "transaction": {
        "amount": 50000, 
        "loc": "London", 
        "timestamp": "2026-02-04T12:00:00"
    },
    "user_baseline": {
        "mean_amt": 1000, 
        "std_amt": 500, 
        "last_loc": "Dubai", 
        "last_time": "2026-02-04T10:00:00"
    }
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error accessing API: {e}")
