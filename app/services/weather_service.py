import httpx
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
from typing import Optional

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
HISTORY_URL = "https://history.openweathermap.org/data/3.0/history/timemachine"

# Free alternative: Open-Meteo (no API key required, 80+ years of historical data)
OPEN_METEO_BASE = "https://api.open-meteo.com/v1"
OPEN_METEO_HISTORY = "https://archive-api.open-meteo.com/v1/archive"
OPEN_METEO_FORECAST = "https://api.open-meteo.com/v1/forecast"

async def reverse_geocode(lat: float, lon: float):
    """
    Reverse geocode coordinates to get location name
    Tries multiple services for better accuracy, especially for Indian locations
    """
    try:
        # Method 1: Try Nominatim (OpenStreetMap) - Best for Indian locations
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    "https://nominatim.openstreetmap.org/reverse",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "format": "json",
                        "addressdetails": 1,
                        "accept-language": "en"
                    },
                    headers={"User-Agent": "SoilCropRecommender/1.0"}
                )
                if response.status_code == 200:
                    data = response.json()
                    address = data.get("address", {})
                    
                    # Build location name prioritizing village/town, then district, then state
                    location_parts = []
                    
                    # For Indian locations, prioritize these fields
                    if address.get("village"):
                        location_parts.append(address["village"])
                    elif address.get("town"):
                        location_parts.append(address["town"])
                    elif address.get("city"):
                        location_parts.append(address["city"])
                    elif address.get("suburb"):
                        location_parts.append(address["suburb"])
                    
                    # Add district/county
                    if address.get("county") or address.get("district"):
                        district = address.get("county") or address.get("district")
                        if district and district not in location_parts:
                            location_parts.append(district)
                    
                    # Add state if in India
                    if address.get("state"):
                        state = address["state"]
                        # For Indian states, we might want to include it
                        if address.get("country") == "India" and len(location_parts) == 0:
                            location_parts.append(state)
                    
                    if location_parts:
                        location_name = ", ".join(location_parts)
                        print(f"✅ Nominatim reverse geocode: {location_name}")
                        return location_name
                    
                    # Fallback to display_name if address parsing fails
                    display_name = data.get("display_name", "")
                    if display_name:
                        # Extract first part (usually the most specific location)
                        parts = display_name.split(",")
                        if len(parts) > 0:
                            return parts[0].strip()
            except Exception as e:
                print(f"⚠️ Nominatim reverse geocode failed: {e}")
        
        # Method 2: Try OpenWeather geocoding (if API key available)
        if API_KEY and API_KEY != "dummy_key_replace_later":
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get(
                        "http://api.openweathermap.org/geo/1.0/reverse",
                        params={"lat": lat, "lon": lon, "limit": 5, "appid": API_KEY}
                    )
                    if response.status_code == 200:
                        data = response.json()
                        if data and len(data) > 0:
                            # Try to find Indian location first
                            for location in data:
                                if location.get("country") == "IN":
                                    name = location.get("name", "")
                                    state = location.get("state", "")
                                    if name:
                                        if state and state not in name:
                                            return f"{name}, {state}"
                                        return name
                            
                            # If no Indian location, use first result
                            return data[0].get("name", "")
            except Exception as e:
                print(f"⚠️ OpenWeather reverse geocode failed: {e}")
        
        # Method 3: Fallback to Open-Meteo geocoding (free, no API key)
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Use search API with coordinates to find nearest location
                response = await client.get(
                    "https://geocoding-api.open-meteo.com/v1/search",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "count": 5,
                        "language": "en"
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    if results:
                        # Try to find Indian location first
                        for result in results:
                            if result.get("country_code") == "IN":
                                name = result.get("name", "")
                                admin1 = result.get("admin1", "")  # State
                                if name:
                                    if admin1 and admin1 not in name:
                                        return f"{name}, {admin1}"
                                    return name
                        
                        # If no Indian location, use first result
                        first_result = results[0]
                        name = first_result.get("name", "")
                        admin1 = first_result.get("admin1", "")
                        if name:
                            if admin1 and admin1 not in name:
                                return f"{name}, {admin1}"
                            return name
        except Exception as e:
            print(f"⚠️ Open-Meteo reverse geocode failed: {e}")
        
    except Exception as e:
        print(f"❌ Reverse geocode error: {e}")
    
    # Final fallback: return coordinates as location
    return f"{lat:.4f}, {lon:.4f}"

async def fetch_weather_openmeteo(lat: float, lon: float):
    """Fetch current weather using Open-Meteo (FREE, no API key required)"""
    try:
        city_name = await reverse_geocode(lat, lon)
        location_display = city_name if city_name else f"{lat:.2f}, {lon:.2f}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPEN_METEO_BASE + "/forecast", params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m",
                "hourly": "precipitation",
                "timezone": "auto"
            })
            
            response.raise_for_status()
            data = response.json()
            
            current = data.get("current", {})
            hourly = data.get("hourly", {})
            
            # Get precipitation from hourly data (last hour)
            hourly_precip = hourly.get("precipitation", [])
            rain_1h = hourly_precip[0] if hourly_precip else 0.0
            
            # Weather code to description mapping (simplified)
            weather_code = current.get("weather_code", 0)
            weather_descriptions = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Foggy", 48: "Depositing rime fog",
                51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
                56: "Light freezing drizzle", 57: "Dense freezing drizzle",
                61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                66: "Light freezing rain", 67: "Heavy freezing rain",
                71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
                77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
                82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
                95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            }
            weather_desc = weather_descriptions.get(weather_code, "Unknown")
            weather_main = "Rain" if weather_code in [61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99] else "Clear"
            
            return {
                "location": location_display,
                "source": "Open-Meteo (Free)",
                "temperature": current.get("temperature_2m", 0),
                "humidity": current.get("relative_humidity_2m", 0),
                "rain_1h": rain_1h,
                "rain_3h": rain_1h * 3,  # Estimate
                "rain": rain_1h,
                "weather": weather_desc,
                "weather_main": weather_main,
                "wind_speed": current.get("wind_speed_10m", 0.0),
                "wind_direction": current.get("wind_direction_10m", 0)
            }
    except Exception as e:
        print(f"❌ Open-Meteo weather fetch error: {e}")
        return {"error": str(e)}

async def fetch_weather(lat: float, lon: float):
    """Fetch current weather - tries OpenWeather first, falls back to Open-Meteo"""
    # Try OpenWeather API first (if API key available)
    if API_KEY and API_KEY != "dummy_key_replace_later":
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(BASE_URL, params={
                    "lat": lat,
                    "lon": lon,
                    "appid": API_KEY,
                    "units": "metric"
                })
                
                # Handle rate limiting (429 error)
                if response.status_code == 429:
                    # Fallback to Open-Meteo on rate limit
                    print("⚠️ OpenWeather rate limit reached, using Open-Meteo fallback")
                    return await fetch_weather_openmeteo(lat, lon)
                
                # Handle API key errors
                if response.status_code == 401:
                    # Fallback to Open-Meteo on invalid key
                    print("⚠️ OpenWeather API key invalid, using Open-Meteo fallback")
                    return await fetch_weather_openmeteo(lat, lon)
                
                response.raise_for_status()
                data = response.json()

                # Get rainfall data (1h = last hour, 3h = last 3 hours if available)
                rain_1h = data.get("rain", {}).get("1h", 0.0)
                rain_3h = data.get("rain", {}).get("3h", 0.0)

                return {
                    "location": data.get("name"),
                    "source": "OpenWeather",
                    "temperature": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "rain_1h": rain_1h,  # Rainfall in last hour (mm)
                    "rain_3h": rain_3h,  # Rainfall in last 3 hours (mm)
                    "rain": rain_1h if rain_1h > 0 else rain_3h,  # Use 1h if available, else 3h
                    "weather": data["weather"][0]["description"],
                    "weather_main": data["weather"][0].get("main", ""),  # Rain, Snow, etc.
                    "wind_speed": data.get("wind", {}).get("speed", 0.0),
                    "wind_direction": data.get("wind", {}).get("deg", 0)
                }
        except httpx.HTTPStatusError as e:
            # Fallback to Open-Meteo on HTTP errors
            print(f"⚠️ OpenWeather error ({e.response.status_code}), using Open-Meteo fallback")
            return await fetch_weather_openmeteo(lat, lon)
        except Exception as e:
            # Fallback to Open-Meteo on any other error
            print(f"⚠️ OpenWeather error: {e}, using Open-Meteo fallback")
            return await fetch_weather_openmeteo(lat, lon)
    
    # No API key or OpenWeather failed - use Open-Meteo
    print("ℹ️ Using Open-Meteo (free, no API key required)")
    return await fetch_weather_openmeteo(lat, lon)

async def fetch_weather_forecast_openmeteo(lat: float, lon: float):
    """Fetch weather forecast using Open-Meteo (FREE, no API key required)"""
    try:
        city_name = await reverse_geocode(lat, lon)
        location_display = city_name if city_name else f"{lat:.2f}, {lon:.2f}"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(OPEN_METEO_FORECAST, params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum,weather_code",
                "hourly": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
                "timezone": "auto",
                "forecast_days": 7  # 7 days forecast
            })
            
            response.raise_for_status()
            data = response.json()
            
            daily_data = data.get("daily", {})
            hourly_data = data.get("hourly", {})
            
            if not daily_data or not daily_data.get("time"):
                return {"error": "No forecast data available"}
            
            # Weather code descriptions
            weather_descriptions = {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Foggy", 48: "Depositing rime fog",
                51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
                61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
                80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
                95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            }
            
            # Process daily forecast
            times = daily_data.get("time", [])
            temps_max = daily_data.get("temperature_2m_max", [])
            temps_min = daily_data.get("temperature_2m_min", [])
            temps_mean = daily_data.get("temperature_2m_mean", [])
            precip = daily_data.get("precipitation_sum", [])
            rain = daily_data.get("rain_sum", [])
            weather_codes = daily_data.get("weather_code", [])
            
            daily_summary = []
            for i in range(min(7, len(times))):  # Up to 7 days
                weather_code = weather_codes[i] if i < len(weather_codes) else 0
                weather_desc = weather_descriptions.get(weather_code, "Unknown")
                
                daily_summary.append({
                    "date": times[i],
                    "min_temp": temps_min[i] if i < len(temps_min) else 0,
                    "max_temp": temps_max[i] if i < len(temps_max) else 0,
                    "avg_temp": temps_mean[i] if i < len(temps_mean) else 0,
                    "avg_humidity": 0,  # Not available in daily data
                    "total_rainfall": rain[i] if i < len(rain) and rain[i] else (precip[i] if i < len(precip) else 0),
                    "max_rainfall": rain[i] if i < len(rain) and rain[i] else (precip[i] if i < len(precip) else 0),
                    "avg_rainfall_probability": 0,  # Not directly available
                    "max_rainfall_probability": 0,
                    "avg_wind_speed": 0,  # Not in daily data
                    "conditions": weather_desc
                })
            
            # Process hourly data for detailed forecast (next 24 hours)
            hourly_times = hourly_data.get("time", [])
            hourly_temps = hourly_data.get("temperature_2m", [])
            hourly_humidity = hourly_data.get("relative_humidity_2m", [])
            hourly_precip = hourly_data.get("precipitation", [])
            hourly_weather = hourly_data.get("weather_code", [])
            hourly_wind = hourly_data.get("wind_speed_10m", [])
            
            detailed = []
            for i in range(min(24, len(hourly_times))):
                weather_code = hourly_weather[i] if i < len(hourly_weather) else 0
                weather_desc = weather_descriptions.get(weather_code, "Unknown")
                
                detailed.append({
                    "datetime": hourly_times[i],
                    "temperature": hourly_temps[i] if i < len(hourly_temps) else 0,
                    "humidity": hourly_humidity[i] if i < len(hourly_humidity) else 0,
                    "rain_3h": hourly_precip[i] if i < len(hourly_precip) else 0,
                    "rain": hourly_precip[i] if i < len(hourly_precip) else 0,
                    "rainfall_probability": 0,  # Not available
                    "weather": weather_desc,
                    "weather_main": "Rain" if weather_code in [61, 63, 65, 80, 81, 82, 95, 96, 99] else "Clear",
                    "wind_speed": hourly_wind[i] if i < len(hourly_wind) else 0,
                    "wind_direction": 0,  # Not in hourly data
                    "pressure": 0,
                    "clouds": 0
                })
            
            return {
                "location": location_display,
                "country": "",
                "source": "Open-Meteo (Free)",
                "forecast": daily_summary,
                "days_available": len(daily_summary),
                "detailed": detailed
            }
    except Exception as e:
        print(f"❌ Open-Meteo forecast error: {e}")
        return {"error": str(e)}

async def fetch_weather_forecast(lat: float, lon: float):
    """Fetch weather forecast - tries OpenWeather first, falls back to Open-Meteo"""
    # Try OpenWeather API first (if API key available)
    if API_KEY and API_KEY != "dummy_key_replace_later":
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Free plan provides 5 days of forecast (40 data points: 5 days * 8 forecasts/day)
                response = await client.get(FORECAST_URL, params={
                    "lat": lat,
                    "lon": lon,
                    "appid": API_KEY,
                    "units": "metric",
                    "cnt": 40  # 5 days * 8 forecasts per day = 40 (3-hour intervals)
                })
                
                # Handle rate limiting (429 error)
                if response.status_code == 429:
                    print("⚠️ OpenWeather rate limit reached, using Open-Meteo fallback")
                    return await fetch_weather_forecast_openmeteo(lat, lon)
                
                # Handle API key errors
                if response.status_code == 401:
                    print("⚠️ OpenWeather API key invalid, using Open-Meteo fallback")
                    return await fetch_weather_forecast_openmeteo(lat, lon)
                
                response.raise_for_status()
                data = response.json()
                
                # Check if we have forecast data
                forecast_list = data.get("list", [])
                city_info = data.get("city", {})
                city_name = city_info.get("name", "Unknown")
                if not city_name or city_name.strip() == "":
                    city_name = "Unknown"
                country_code = city_info.get("country", "")
                
                if not forecast_list:
                    print("⚠️ No OpenWeather forecast data, using Open-Meteo fallback")
                    return await fetch_weather_forecast_openmeteo(lat, lon)
                
                # Process forecast data
                forecasts = []
                for item in forecast_list:
                    rain_3h = item.get("rain", {}).get("3h", 0.0)
                    weather_main = item["weather"][0].get("main", "")
                    pop = item.get("pop", 0.0) * 100  # Probability of precipitation (0-100%)
                    
                    forecasts.append({
                        "datetime": item["dt_txt"],
                        "temperature": item["main"]["temp"],
                        "humidity": item["main"]["humidity"],
                        "rain_3h": rain_3h,  # Rainfall in 3-hour period (mm)
                        "rain": rain_3h,  # Alias for compatibility
                        "rainfall_probability": pop,  # Probability of precipitation (%)
                        "weather": item["weather"][0]["description"],
                        "weather_main": weather_main,  # Rain, Snow, Clear, etc.
                        "wind_speed": item.get("wind", {}).get("speed", 0.0),
                        "wind_direction": item.get("wind", {}).get("deg", 0),
                        "pressure": item.get("main", {}).get("pressure", 0),
                        "clouds": item.get("clouds", {}).get("all", 0)  # Cloud coverage %
                    })
                
                # Group by day and get daily summary
                daily_forecasts = {}
                for forecast in forecasts:
                    date = forecast["datetime"].split()[0]
                    if date not in daily_forecasts:
                        daily_forecasts[date] = {
                            "date": date,
                            "temperatures": [],
                            "humidity": [],
                            "rainfall": [],
                            "rainfall_probability": [],
                            "weather": [],
                            "wind_speed": []
                        }
                    daily_forecasts[date]["temperatures"].append(forecast["temperature"])
                    daily_forecasts[date]["humidity"].append(forecast["humidity"])
                    daily_forecasts[date]["rainfall"].append(forecast["rain_3h"])
                    daily_forecasts[date]["rainfall_probability"].append(forecast.get("rainfall_probability", 0))
                    daily_forecasts[date]["weather"].append(forecast["weather"])
                    daily_forecasts[date]["wind_speed"].append(forecast.get("wind_speed", 0))
                
                # Calculate daily averages (Free plan: 5 days max)
                daily_summary = []
                if daily_forecasts:
                    for date, data in sorted(daily_forecasts.items())[:5]:  # Free plan: 5 days
                        if data["temperatures"]:  # Ensure we have data
                            daily_summary.append({
                                "date": date,
                                "min_temp": min(data["temperatures"]),
                                "max_temp": max(data["temperatures"]),
                                "avg_temp": sum(data["temperatures"]) / len(data["temperatures"]),
                                "avg_humidity": sum(data["humidity"]) / len(data["humidity"]) if data["humidity"] else 0,
                                "total_rainfall": sum(data["rainfall"]),  # Total rainfall for the day (mm)
                                "max_rainfall": max(data["rainfall"]) if data["rainfall"] else 0,  # Max rainfall in any 3h period
                                "avg_rainfall_probability": sum(data["rainfall_probability"]) / len(data["rainfall_probability"]) if data["rainfall_probability"] else 0,
                                "max_rainfall_probability": max(data["rainfall_probability"]) if data["rainfall_probability"] else 0,
                                "avg_wind_speed": sum(data["wind_speed"]) / len(data["wind_speed"]) if data["wind_speed"] else 0,
                                "conditions": max(set(data["weather"]), key=data["weather"].count) if data["weather"] else "Unknown"  # Most common
                            })
                
                if not daily_summary:
                    print("⚠️ No OpenWeather daily summary, using Open-Meteo fallback")
                    return await fetch_weather_forecast_openmeteo(lat, lon)
                
                return {
                    "location": city_name,
                    "country": country_code,
                    "source": "OpenWeather",
                    "forecast": daily_summary,
                    "days_available": len(daily_summary),  # Will be 5 for free plan
                    "detailed": forecasts[:24]  # Next 24 hours (3-hour intervals)
                }
        except httpx.HTTPStatusError as e:
            print(f"⚠️ OpenWeather error ({e.response.status_code}), using Open-Meteo fallback")
            return await fetch_weather_forecast_openmeteo(lat, lon)
        except Exception as e:
            print(f"⚠️ OpenWeather error: {e}, using Open-Meteo fallback")
            return await fetch_weather_forecast_openmeteo(lat, lon)
    
    # No API key or OpenWeather failed - use Open-Meteo
    print("ℹ️ Using Open-Meteo for forecast (free, no API key required)")
    return await fetch_weather_forecast_openmeteo(lat, lon)

async def fetch_historical_weather(lat: float, lon: float, days_ago: int = 1):
    """
    Fetch historical weather data (Note: May require paid plan)
    Free plan: Limited historical data (last 2 days only)
    Paid plans: Full historical data from 1979 to present
    """
    try:
        if not API_KEY or API_KEY == "dummy_key_replace_later":
            return {"error": "OpenWeather API key not configured. Please set OPENWEATHER_API_KEY in .env"}
        
        # Calculate timestamp for the requested date
        target_date = datetime.now() - timedelta(days=days_ago)
        unix_timestamp = int(target_date.timestamp())
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(HISTORY_URL, params={
                "lat": lat,
                "lon": lon,
                "dt": unix_timestamp,
                "appid": API_KEY,
                "units": "metric"
            })
            
            # Handle rate limiting (429 error)
            if response.status_code == 429:
                return {
                    "error": "Rate limit exceeded. Free plan allows 60 calls/minute. Please wait a moment.",
                    "rate_limit": True
                }
            
            # Handle API key errors (401) - Could also mean subscription required
            if response.status_code == 401:
                # Try to parse error message
                try:
                    error_data = response.json()
                    error_msg = error_data.get("message", "")
                    if "subscription" in error_msg.lower() or "plan" in error_msg.lower():
                        return {
                            "error": "Historical weather data requires a paid subscription plan. Free plan does not include History API access.",
                            "subscription_required": True,
                            "note": "The History API is only available with paid plans. Free plan includes current weather and 5-day forecast only."
                        }
                except:
                    pass
                return {
                    "error": "Invalid API key or subscription required. Historical weather data requires a paid subscription plan.",
                    "auth_error": True,
                    "subscription_required": True,
                    "note": "Free plan: Current weather + 5-day forecast only. History API requires paid subscription."
                }
            
            # Handle subscription errors (403 - requires paid plan)
            if response.status_code == 403:
                return {
                    "error": "Historical weather data requires a paid subscription plan. Free plan has limited access.",
                    "subscription_required": True,
                    "note": "Free plan may only access last 2 days. For full historical data (1979-present), upgrade to a paid plan."
                }
            
            response.raise_for_status()
            data = response.json()
            
            # Process historical data - OpenWeather History API format
            historical_data = data.get("data", [])
            if not historical_data:
                return {
                    "error": "No historical data available for this date.",
                    "date": target_date.strftime("%Y-%m-%d")
                }
            
            # Get the first data point (closest to requested time)
            item = historical_data[0]
            main_data = item.get("main", {})
            rain_data = item.get("rain", {})
            weather_data = item.get("weather", [{}])[0] if item.get("weather") else {}
            
            rain_1h = rain_data.get("1h", 0.0) if isinstance(rain_data, dict) else 0.0
            rain_3h = rain_data.get("3h", 0.0) if isinstance(rain_data, dict) else 0.0
            
            return {
                "date": target_date.strftime("%Y-%m-%d"),
                "timestamp": unix_timestamp,
                "location": data.get("location", {}).get("name", "Unknown"),
                "temperature": main_data.get("temp", 0),
                "min_temp": main_data.get("temp_min", main_data.get("temp", 0)),
                "max_temp": main_data.get("temp_max", main_data.get("temp", 0)),
                "humidity": main_data.get("humidity", 0),
                "rain_1h": rain_1h,
                "rain_3h": rain_3h,
                "rain": rain_1h if rain_1h > 0 else rain_3h,
                "weather": weather_data.get("description", "Unknown"),
                "wind_speed": item.get("wind", {}).get("speed", 0) if isinstance(item.get("wind"), dict) else 0,
                "wind_direction": item.get("wind", {}).get("deg", 0) if isinstance(item.get("wind"), dict) else 0,
                "pressure": main_data.get("pressure", 0),
                "clouds": item.get("clouds", {}).get("all", 0) if isinstance(item.get("clouds"), dict) else 0
            }
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 403:
            return {
                "error": "Historical weather data requires a paid subscription plan.",
                "subscription_required": True
            }
        if e.response.status_code == 401:
            return {
                "error": "Historical weather data requires a paid subscription plan. Free plan does not include History API access.",
                "subscription_required": True,
                "note": "Free plan includes: Current weather + 5-day forecast. History API requires paid subscription."
            }
        if e.response.status_code == 429:
            return {"error": "Rate limit exceeded. Please wait a moment.", "rate_limit": True}
        return {"error": f"HTTP error {e.response.status_code}: {str(e)}"}
    except Exception as e:
        print(f"❌ Historical weather error: {e}")
        return {"error": str(e)}

async def fetch_historical_rainfall_range(lat: float, lon: float, days: int = 7):
    """
    Fetch historical rainfall data for the last N days
    Note: Free plan may have limited access (last 2 days only)
    """
    try:
        if not API_KEY or API_KEY == "dummy_key_replace_later":
            return {"error": "OpenWeather API key not configured. Please set OPENWEATHER_API_KEY in .env"}
        
        historical_data = []
        errors = []
        
        # Try to fetch data for each day (limited to last 2 days on free plan)
        max_days = min(days, 2)  # Free plan limit
        
        for day_offset in range(max_days):
            try:
                result = await fetch_historical_weather(lat, lon, days_ago=day_offset + 1)
                if "error" in result:
                    if result.get("subscription_required"):
                        errors.append(f"Day {day_offset + 1}: {result['error']}")
                        break  # Stop if subscription required
                    else:
                        errors.append(f"Day {day_offset + 1}: {result.get('error', 'Unknown error')}")
                else:
                    historical_data.append(result)
            except Exception as e:
                errors.append(f"Day {day_offset + 1}: {str(e)}")
        
        if not historical_data and errors:
            return {
                "error": "Could not fetch historical data. " + "; ".join(errors[:3]),
                "subscription_required": any("subscription" in str(e).lower() for e in errors)
            }
        
        return {
            "location": historical_data[0].get("location", "Unknown") if historical_data else "Unknown",
            "days_requested": days,
            "days_available": len(historical_data),
            "data": historical_data,
            "warnings": errors if errors else None
        }
    except Exception as e:
        print(f"❌ Historical rainfall range error: {e}")
        return {"error": str(e)}

async def fetch_historical_weather_openmeteo(lat: float, lon: float, days_ago: int = 1, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Fetch historical weather data using Open-Meteo (FREE, no API key required)
    Provides 80+ years of historical weather data
    
    Args:
        lat: Latitude
        lon: Longitude
        days_ago: Days ago (used if start_date/end_date not provided)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    try:
        # Get city name from coordinates
        city_name = await reverse_geocode(lat, lon)
        location_display = city_name if city_name else f"{lat:.2f}, {lon:.2f}"
        
        # Use provided dates or calculate from days_ago
        if start_date and end_date:
            date_str = start_date
            end_date_str = end_date
        else:
            target_date = datetime.now() - timedelta(days=days_ago)
            date_str = target_date.strftime("%Y-%m-%d")
            end_date_str = date_str
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Open-Meteo Archive API - FREE, no API key needed
            # Fixed parameters to match Open-Meteo API requirements
            response = await client.get(OPEN_METEO_HISTORY, params={
                "latitude": lat,
                "longitude": lon,
                "start_date": date_str,
                "end_date": end_date_str,
                "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum",
                "timezone": "auto"
            })
            
            response.raise_for_status()
            data = response.json()
            
            daily_data = data.get("daily", {})
            if not daily_data or not daily_data.get("time"):
                return {
                    "error": "No historical data available for this date.",
                    "date": date_str
                }
            
            # Get first day's data
            idx = 0
            daily_times = daily_data.get("time", [])
            if not daily_times:
                return {"error": "No data available for this date"}
            
            # Get daily values
            temps_min = daily_data.get("temperature_2m_min", [])
            temps_max = daily_data.get("temperature_2m_max", [])
            temps_mean = daily_data.get("temperature_2m_mean", [])
            precip_sum = daily_data.get("precipitation_sum", [])
            rain_sum = daily_data.get("rain_sum", [])
            
            min_temp = temps_min[idx] if temps_min and len(temps_min) > idx else 0
            max_temp = temps_max[idx] if temps_max and len(temps_max) > idx else 0
            mean_temp = temps_mean[idx] if temps_mean and len(temps_mean) > idx else (min_temp + max_temp) / 2
            total_precip = precip_sum[idx] if precip_sum and len(precip_sum) > idx else 0
            total_rain = rain_sum[idx] if rain_sum and len(rain_sum) > idx else 0
            
            return {
                "date": date_str,
                "location": location_display,
                "source": "Open-Meteo (Free)",
                "temperature": mean_temp,
                "min_temp": min_temp,
                "max_temp": max_temp,
                "humidity": 0,  # Not available in daily data
                "rain": total_rain if total_rain > 0 else total_precip,
                "rain_1h": 0,  # Not available in daily data
                "rain_3h": 0,  # Not available in daily data
                "precipitation": total_precip,
                "weather": "Rainy" if (total_rain if total_rain > 0 else total_precip) > 0 else "Clear",
                "wind_speed": 0,  # Not available in free tier daily data
                "wind_direction": 0,
                "pressure": 0,  # Not available in free tier
                "clouds": 0
            }
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error {e.response.status_code}: {str(e)}"}
    except Exception as e:
        print(f"❌ Open-Meteo historical error: {e}")
        return {"error": str(e)}

async def fetch_historical_rainfall_range_openmeteo(lat: float, lon: float, days: int = 7, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Fetch historical rainfall data for multiple days using Open-Meteo (FREE)
    
    Args:
        lat: Latitude
        lon: Longitude
        days: Number of days (used if start_date/end_date not provided)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
    """
    try:
        # Get city name from coordinates
        city_name = await reverse_geocode(lat, lon)
        location_display = city_name if city_name else f"{lat:.2f}, {lon:.2f}"
        
        # Use provided dates or calculate from days
        if start_date and end_date:
            start_str = start_date
            end_str = end_date
        else:
            end_date_obj = datetime.now() - timedelta(days=1)
            start_date_obj = end_date_obj - timedelta(days=days - 1)
            start_str = start_date_obj.strftime("%Y-%m-%d")
            end_str = end_date_obj.strftime("%Y-%m-%d")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Fixed parameters to match Open-Meteo API requirements
            response = await client.get(OPEN_METEO_HISTORY, params={
                "latitude": lat,
                "longitude": lon,
                "start_date": start_str,
                "end_date": end_str,
                "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,rain_sum",
                "timezone": "auto"
            })
            
            response.raise_for_status()
            data = response.json()
            
            daily_data = data.get("daily", {})
            if not daily_data or not daily_data.get("time"):
                return {"error": "No historical data available"}
            
            historical_data = []
            times = daily_data.get("time", [])
            temps_max = daily_data.get("temperature_2m_max", [])
            temps_min = daily_data.get("temperature_2m_min", [])
            temps_mean = daily_data.get("temperature_2m_mean", [])
            precip = daily_data.get("precipitation_sum", [])
            rain = daily_data.get("rain_sum", [])
            
            for i in range(len(times)):
                # Ensure we don't go out of bounds
                if i < len(times):
                    historical_data.append({
                        "date": times[i],
                        "location": location_display,
                        "source": "Open-Meteo (Free)",
                        "temperature": temps_mean[i] if temps_mean and i < len(temps_mean) else 0,
                        "min_temp": temps_min[i] if temps_min and i < len(temps_min) else 0,
                        "max_temp": temps_max[i] if temps_max and i < len(temps_max) else 0,
                        "humidity": 0,  # Daily average not directly available
                        "rain": rain[i] if rain and i < len(rain) and rain[i] is not None else (precip[i] if precip and i < len(precip) and precip[i] is not None else 0),
                        "rain_1h": 0,
                        "rain_3h": 0,
                        "precipitation": precip[i] if precip and i < len(precip) and precip[i] is not None else 0,
                        "weather": "Rainy" if (rain[i] if rain and i < len(rain) and rain[i] is not None else 0) > 0 else "Clear",
                        "wind_speed": 0,
                        "wind_direction": 0,
                        "pressure": 0,
                        "clouds": 0
                    })
            
            return {
                "location": location_display,
                "source": "Open-Meteo (Free)",
                "days_requested": days,
                "days_available": len(historical_data),
                "data": historical_data
            }
    except Exception as e:
        print(f"❌ Open-Meteo range error: {e}")
        return {"error": str(e)}
