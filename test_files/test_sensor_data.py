import requests
import json
from datetime import datetime

# Test data
test_data = {
    "Soil": 45,
    "Temp": 25.5,
    "Hum": 60.2
}

# Send POST request to the soil-data endpoint
try:
    response = requests.post(
        "http://10.238.141.218:8000/soil-data",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Now test the dashboard endpoint
    dashboard_response = requests.get("http://10.238.141.218:8000/npk-dashboard")
    print(f"Dashboard Status Code: {dashboard_response.status_code}")
    print(f"Dashboard Response: {json.dumps(dashboard_response.json(), indent=2)}")
    
except Exception as e:
    print(f"Error: {e}")