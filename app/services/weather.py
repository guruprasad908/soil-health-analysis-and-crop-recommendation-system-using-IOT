import requests
import os

def get_rainfall(location: str):
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract rainfall data (default to 0 if not available)
        rainfall = data.get("rain", {}).get("1h", 0.0)
        return rainfall
    except Exception as e:
        print(f"Weather API Error: {e}")
        return 0.0
