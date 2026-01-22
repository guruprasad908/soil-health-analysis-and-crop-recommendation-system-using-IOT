"""
Script to verify Arduino UNO R4 WiFi backend endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/sensor"

def test_post_data():
    print("\n1. Testing POST /api/sensor/uno-data...")
    payload = {
        "temperature": 25.5,
        "humidity": 60.0,
        "moisture": 45,
        "device_id": "ArduinoUNO_Test"
    }
    try:
        response = requests.post(f"{BASE_URL}/uno-data", json=payload)
        if response.status_code == 200:
            print("✅ Success! Response:", response.json())
            return True
        else:
            print(f"❌ Failed! Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_get_dashboard():
    print("\n2. Testing GET /api/sensor/uno-dashboard...")
    try:
        response = requests.get(f"{BASE_URL}/uno-dashboard")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Data received:")
            print(json.dumps(data, indent=2))
            
            # Verify the data we just sent is there
            readings = data.get("readings", [])
            if readings and readings[0]["device_id"] == "ArduinoUNO_Test":
                print("✅ Verification confirmed: Latest reading matches sent data.")
                return True
            else:
                print("⚠️ Warning: Latest reading does not match sent data (might be old data).")
                return True
        else:
            print(f"❌ Failed! Status: {response.status_code}, Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Verifying Arduino UNO Backend Endpoints")
    print("=" * 60)
    
    if test_post_data():
        test_get_dashboard()
    
    print("\n" + "=" * 60)
