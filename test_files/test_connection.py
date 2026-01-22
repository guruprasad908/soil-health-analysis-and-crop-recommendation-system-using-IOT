import requests
import time

# Test if the server is responding
try:
    print("Testing connection to FastAPI server...")
    response = requests.get("http://10.238.141.218:8000/", timeout=5)
    print(f"Server response: {response.status_code}")
    print(f"Response content: {response.json()}")
except Exception as e:
    print(f"Error connecting to server: {e}")

# Test the soil-data endpoint
try:
    print("\nTesting soil-data endpoint...")
    test_data = {
        "Soil": 50,
        "Temp": 25.0,
        "Hum": 60.0
    }
    response = requests.post(
        "http://10.238.141.218:8000/soil-data",
        json=test_data,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    print(f"Soil-data POST response: {response.status_code}")
    print(f"Response content: {response.json()}")
except Exception as e:
    print(f"Error sending data to soil-data endpoint: {e}")

# Test the dashboard endpoint
try:
    print("\nTesting npk-dashboard endpoint...")
    response = requests.get("http://10.238.141.218:8000/npk-dashboard", timeout=5)
    print(f"Dashboard GET response: {response.status_code}")
    print(f"Response content: {response.json()}")
except Exception as e:
    print(f"Error getting dashboard data: {e}")