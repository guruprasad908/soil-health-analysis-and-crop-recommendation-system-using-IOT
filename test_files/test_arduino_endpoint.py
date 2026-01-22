import requests
import json
from datetime import datetime

# Test data matching the Arduino format
test_data = {
    "Soil": 58,
    "Temp": 27.9,
    "Hum": 55.4
}

# Send POST request to the soil-data endpoint
try:
    response = requests.post(
        "http://localhost:8000/soil-data",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Now test the dashboard endpoint to see if the data was stored
    dashboard_response = requests.get("http://localhost:8000/npk-dashboard")
    print(f"\nDashboard Status Code: {dashboard_response.status_code}")
    dashboard_data = dashboard_response.json()
    print(f"Total readings: {dashboard_data['total_readings']}")
    if dashboard_data['readings']:
        latest_reading = dashboard_data['readings'][0]
        print(f"Latest reading: Soil={latest_reading['N']}, Temp={latest_reading['P']}, Hum={latest_reading['K']}")
    
except Exception as e:
    print(f"Error: {e}")