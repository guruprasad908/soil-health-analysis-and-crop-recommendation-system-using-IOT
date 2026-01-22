import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Live Weather", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>🌦 Live Weather Forecast</h1>", unsafe_allow_html=True)
st.info("ℹ️ **Free Plan**: 1000 calls/day, 60 calls/minute. Forecast limited to 5 days.")

location = st.text_input("Enter your location (e.g., Pune, Delhi)", value="Pune")

# Styling success box for dark mode
st.markdown("""
<style>
.stAlert {
    background-color: #14532d !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Geocoding
def geocode(city):
    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        response = requests.get(geo_url)
        data = response.json()
        if data and isinstance(data, list):
            return data[0]["lat"], data[0]["lon"]
    except:
        return None, None
    return None, None

# Initialize session state
if 'show_history' not in st.session_state:
    st.session_state.show_history = False

col1, col2, col3 = st.columns(3)
with col1:
    fetch_current = st.button("🔍 Fetch Current Weather")
with col2:
    fetch_forecast = st.button("📅 Fetch 5-Day Forecast")
with col3:
    if st.button("📜 Historical Weather"):
        st.session_state.show_history = not st.session_state.show_history

if fetch_current:
    lat, lon = geocode(location)

    if lat and lon:
        try:
            res = requests.get(f"{API_BASE_URL}/weather?lat={lat}&lon={lon}")
            weather = res.json()

            if weather.get("error"):
                error_msg = weather.get("error", "Could not fetch weather data")
                if weather.get("rate_limit"):
                    st.error(f"⚠️ {error_msg}")
                    st.warning("💡 **Tip**: Free plan allows 60 calls/minute. Please wait a moment before trying again.")
                elif weather.get("auth_error"):
                    st.error(f"⚠️ {error_msg}")
                    st.info("💡 **Setup**: Add your OpenWeather API key to the `.env` file as `OPENWEATHER_API_KEY=your_key`")
                else:
                    st.error(f"⚠️ {error_msg}")
            else:
                temp = weather.get("temperature", "N/A")
                humid = weather.get("humidity", "N/A")
                condition = weather.get("weather", "N/A")
                rain = weather.get("rain", "N/A")
                city = weather.get("location", location)

                # Show location
                st.success(f"📍 Weather in {city}")

                # Main metrics
                col1, col2 = st.columns(2)
                col1.metric("🌡 Temperature", f"{temp} °C" if temp != "N/A" else "N/A")
                col2.metric("💧 Humidity", f"{humid} %" if humid != "N/A" else "N/A")

                # Sky and Rainfall
                st.markdown("---")
                st.markdown(f"### ☁️ Sky Condition\n**{condition.capitalize()}**")
                
                # Enhanced rainfall display
                rain_1h = weather.get("rain_1h", 0)
                rain_3h = weather.get("rain_3h", 0)
                wind_speed = weather.get("wind_speed", 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    if isinstance(rain, (int, float)) and rain > 0:
                        st.metric("🌧 Rainfall (Last Hour)", f"{rain_1h:.2f} mm" if rain_1h > 0 else f"{rain_3h:.2f} mm (3h)")
                    else:
                        st.metric("🌧 Rainfall", "0 mm")
                with col2:
                    st.metric("💨 Wind Speed", f"{wind_speed:.1f} m/s" if wind_speed > 0 else "N/A")
                
                # Rainfall intensity description
                if isinstance(rain, (int, float)) and rain > 0:
                    if rain < 2.5:
                        intensity = "Light rain"
                    elif rain < 7.6:
                        intensity = "Moderate rain"
                    elif rain < 50:
                        intensity = "Heavy rain"
                    else:
                        intensity = "Very heavy rain"
                    st.info(f"💧 **Rainfall Intensity**: {intensity}")

        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")
    else:
        st.warning("⚠️ Could not find that location. Try a nearby city.")

if fetch_forecast:
    lat, lon = geocode(location)
    
    if lat and lon:
        try:
            res = requests.get(f"{API_BASE_URL}/weather-forecast?lat={lat}&lon={lon}")
            forecast = res.json()
            
            if forecast.get("error"):
                error_msg = forecast.get("error", "Could not fetch forecast data")
                if forecast.get("rate_limit"):
                    st.error(f"⚠️ {error_msg}")
                    st.warning("💡 **Tip**: Free plan allows 60 calls/minute. Please wait a moment before trying again.")
                elif forecast.get("auth_error"):
                    st.error(f"⚠️ {error_msg}")
                    st.info("💡 **Setup**: Add your OpenWeather API key to the `.env` file as `OPENWEATHER_API_KEY=your_key`")
                else:
                    st.error(f"⚠️ {error_msg}")
            else:
                city = forecast.get("location", location)
                country = forecast.get("country", "")
                daily_forecast = forecast.get("forecast", [])
                
                if not daily_forecast or len(daily_forecast) == 0:
                    st.warning("⚠️ No forecast data available. This might be due to:")
                    st.info("""
                    - API key not configured (check .env file)
                    - Rate limit exceeded (free plan: 60 calls/minute)
                    - Invalid location
                    - API service temporarily unavailable
                    """)
                else:
                    days_available = len(daily_forecast)
                    st.success(f"📍 {days_available}-Day Forecast for {city}, {country}")
                
                if daily_forecast and len(daily_forecast) > 0:
                    import pandas as pd
                    df = pd.DataFrame(daily_forecast)
                    df['date'] = pd.to_datetime(df['date'])
                    
                    # Display forecast cards
                    st.markdown(f"### 📅 Daily Forecast ({days_available} days)")
                    for day in daily_forecast:
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Date", day['date'])
                        with col2:
                            st.metric("Temperature", f"{day['min_temp']:.1f}°C - {day['max_temp']:.1f}°C")
                        with col3:
                            total_rain = day.get('total_rainfall', 0)
                            max_rain = day.get('max_rainfall', 0)
                            rain_prob = day.get('max_rainfall_probability', 0)
                            if total_rain > 0:
                                st.metric("🌧 Rainfall", f"{total_rain:.1f} mm", 
                                         help=f"Total: {total_rain:.1f}mm | Max 3h: {max_rain:.1f}mm | Probability: {rain_prob:.0f}%")
                            else:
                                st.metric("🌧 Rainfall", "0 mm", 
                                         help=f"Rain probability: {rain_prob:.0f}%")
                        with col4:
                            st.metric("Humidity", f"{day['avg_humidity']:.1f}%")
                        with col5:
                            wind = day.get('avg_wind_speed', 0)
                            st.metric("💨 Wind", f"{wind:.1f} m/s" if wind > 0 else "N/A")
                        
                        # Rainfall details
                        if total_rain > 0 or rain_prob > 0:
                            rain_info = []
                            if total_rain > 0:
                                rain_info.append(f"Total: {total_rain:.1f}mm")
                            if max_rain > 0:
                                rain_info.append(f"Peak (3h): {max_rain:.1f}mm")
                            if rain_prob > 0:
                                rain_info.append(f"Probability: {rain_prob:.0f}%")
                            st.caption(f"🌧 {' | '.join(rain_info)}")
                        
                        st.caption(f"Conditions: {day['conditions']}")
                        st.markdown("---")
                    
                    # Charts
                    st.markdown("### 📈 Forecast Trends")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.line_chart(df.set_index('date')[['min_temp', 'max_temp', 'avg_temp']])
                        st.caption("Temperature Forecast")
                    with col2:
                        # Enhanced rainfall chart
                        if 'total_rainfall' in df.columns:
                            st.bar_chart(df.set_index('date')['total_rainfall'])
                            st.caption("Daily Total Rainfall (mm)")
                    
                    # Detailed hourly rainfall for next 24 hours
                    detailed_forecast = forecast.get("detailed", [])
                    if detailed_forecast:
                        st.markdown("### 🌧 Hourly Rainfall Breakdown (Next 24 Hours)")
                        hourly_rain = []
                        for item in detailed_forecast[:8]:  # Next 24 hours (8 * 3h = 24h)
                            hourly_rain.append({
                                "Time": item.get("datetime", "").split()[1] if " " in item.get("datetime", "") else item.get("datetime", ""),
                                "Date": item.get("datetime", "").split()[0] if " " in item.get("datetime", "") else "",
                                "Rainfall (mm)": item.get("rain_3h", 0),
                                "Probability (%)": item.get("rainfall_probability", 0),
                                "Temperature (°C)": item.get("temperature", 0)
                            })
                        
                        if hourly_rain:
                            import pandas as pd
                            hourly_df = pd.DataFrame(hourly_rain)
                            st.dataframe(hourly_df, use_container_width=True)
                            
                            # Hourly rainfall chart
                            if len(hourly_rain) > 0:
                                st.bar_chart(hourly_df.set_index('Time')['Rainfall (mm)'])
                                st.caption("3-Hour Rainfall Intervals")
        except Exception as e:
            st.error(f"❌ Error fetching forecast: {e}")
    else:
        st.warning("⚠️ Could not find that location. Try a nearby city.")

# Historical Weather Section
if st.session_state.show_history:
    st.markdown("---")
    col_header, col_close = st.columns([5, 1])
    with col_header:
        st.markdown("### 📜 Historical Weather & Rainfall Data")
    with col_close:
        if st.button("❌ Close", key="close_history"):
            st.session_state.show_history = False
            st.rerun()
    
    st.success("✅ **Using FREE Open-Meteo API** - No subscription required! Access to 80+ years of historical weather data.")
    
    lat, lon = geocode(location)
    
    if lat and lon:
        # Date selection method
        date_method = st.radio(
            "Select Date Range Method:",
            ["📅 Select Date Range", "📆 Select Month", "⏮️ Days Ago"],
            horizontal=True
        )
        
        start_date = None
        end_date = None
        days_ago = None
        days_range = None
        
        if date_method == "📅 Select Date Range":
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=datetime.now().date() - timedelta(days=7),
                    max_value=datetime.now().date(),
                    help="Select start date for historical data"
                )
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=datetime.now().date() - timedelta(days=1),
                    max_value=datetime.now().date(),
                    help="Select end date for historical data"
                )
            if start_date > end_date:
                st.error("⚠️ Start date must be before end date!")
        elif date_method == "📆 Select Month":
            col1, col2 = st.columns(2)
            with col1:
                selected_year = st.selectbox("Year", range(2020, datetime.now().year + 1), index=len(range(2020, datetime.now().year + 1)) - 1)
            with col2:
                selected_month = st.selectbox("Month", range(1, 13), index=datetime.now().month - 1)
            
            # Calculate start and end dates for the selected month
            if selected_year == datetime.now().year and selected_month == datetime.now().month:
                start_date = datetime(selected_year, selected_month, 1).date()
                end_date = datetime.now().date() - timedelta(days=1)
            else:
                start_date = datetime(selected_year, selected_month, 1).date()
                # Get last day of month
                if selected_month == 12:
                    end_date = datetime(selected_year + 1, 1, 1).date() - timedelta(days=1)
                else:
                    end_date = datetime(selected_year, selected_month + 1, 1).date() - timedelta(days=1)
        else:  # Days Ago
            col1, col2 = st.columns(2)
            with col1:
                days_ago = st.number_input("Days ago", min_value=1, max_value=36500, value=7, 
                                          help="Open-Meteo: Up to 80+ years of historical data available")
            with col2:
                days_range = st.number_input("Historical range (days)", min_value=1, max_value=365, value=7,
                                            help="Get historical data for multiple days")
        
        col1, col2 = st.columns(2)
        with col1:
            fetch_single = st.button("📅 Get Single Day History (Free)")
        with col2:
            fetch_range = st.button("📊 Get Historical Range (Free)")
        
        if fetch_single:
            try:
                # Build URL with date range or days_ago
                url = f"{API_BASE_URL}/weather-history-free?lat={lat}&lon={lon}"
                if start_date and end_date:
                    url += f"&start_date={start_date}&end_date={end_date}"
                elif days_ago:
                    url += f"&days_ago={days_ago}"
                
                res = requests.get(url)
                history = res.json()
                
                if history.get("error"):
                    error_msg = history.get("error", "Could not fetch historical data")
                    if history.get("subscription_required") or history.get("auth_error"):
                        st.error(f"⚠️ {error_msg}")
                        st.warning("💡 **Subscription Required**: The History API is not included in the free plan.")
                        st.info("""
                        **Free Plan Includes:**
                        - ✅ Current weather
                        - ✅ 5-day forecast
                        - ❌ Historical weather data (requires paid plan)
                        
                        **To Access Historical Data:**
                        Upgrade to a paid OpenWeather subscription plan to access historical weather data (1979-present).
                        """)
                    elif history.get("rate_limit"):
                        st.error(f"⚠️ {error_msg}")
                        st.warning("💡 **Tip**: Free plan allows 60 calls/minute. Please wait a moment before trying again.")
                    else:
                        st.error(f"⚠️ {error_msg}")
                        if "subscription" in error_msg.lower() or "paid" in error_msg.lower():
                            st.info("💡 **Note**: Historical weather data requires a paid subscription plan.")
                else:
                    st.success(f"📍 Historical Weather for {history.get('location', location)} - {history.get('date', 'N/A')}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🌡 Temperature", f"{history.get('temperature', 0):.1f}°C")
                        st.caption(f"Min: {history.get('min_temp', 0):.1f}°C | Max: {history.get('max_temp', 0):.1f}°C")
                    with col2:
                        rain = history.get('rain', 0)
                        st.metric("🌧 Rainfall", f"{rain:.2f} mm" if rain > 0 else "0 mm")
                        if rain > 0:
                            st.caption(f"1h: {history.get('rain_1h', 0):.2f}mm | 3h: {history.get('rain_3h', 0):.2f}mm")
                    with col3:
                        st.metric("💧 Humidity", f"{history.get('humidity', 0):.1f}%")
                    
                    st.markdown("---")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("💨 Wind Speed", f"{history.get('wind_speed', 0):.1f} m/s")
                    with col2:
                        st.metric("☁️ Cloud Coverage", f"{history.get('clouds', 0):.0f}%")
                    
                    st.caption(f"**Conditions**: {history.get('weather', 'Unknown')}")
            except Exception as e:
                st.error(f"❌ Error fetching historical data: {e}")
        
        if fetch_range:
            try:
                # Build URL with date range or days
                url = f"{API_BASE_URL}/weather-history-range?lat={lat}&lon={lon}&use_free=true"
                if start_date and end_date:
                    url += f"&start_date={start_date}&end_date={end_date}"
                elif days_range:
                    url += f"&days={days_range}"
                
                res = requests.get(url)
                history_range = res.json()
                
                if history_range.get("error"):
                    error_msg = history_range.get("error", "Could not fetch historical data")
                    if history_range.get("subscription_required"):
                        st.error(f"⚠️ {error_msg}")
                        st.warning("💡 **Subscription Required**: The History API is not included in the free plan.")
                        st.info("""
                        **Free Plan Includes:**
                        - ✅ Current weather
                        - ✅ 5-day forecast
                        - ❌ Historical weather data (requires paid plan)
                        
                        **To Access Historical Data:**
                        Upgrade to a paid OpenWeather subscription plan to access historical weather data (1979-present).
                        """)
                    else:
                        st.error(f"⚠️ {error_msg}")
                        if "subscription" in error_msg.lower() or "paid" in error_msg.lower() or "401" in str(error_msg):
                            st.info("💡 **Note**: Historical weather data requires a paid subscription plan. The free plan does not include History API access.")
                else:
                    historical_data = history_range.get("data", [])
                    days_available = history_range.get("days_available", 0)
                    
                    st.success(f"📍 Historical Rainfall Data for {history_range.get('location', location)}")
                    st.info(f"📊 **Available**: {days_available} days (Requested: {days_range} days)")
                    
                    if historical_data:
                        import pandas as pd
                        df = pd.DataFrame(historical_data)
                        
                        # Display historical data table
                        st.markdown("### 📋 Historical Data")
                        display_df = df[['date', 'temperature', 'min_temp', 'max_temp', 'rain', 'rain_1h', 'rain_3h', 'humidity', 'wind_speed']].copy()
                        display_df.columns = ['Date', 'Temp (°C)', 'Min (°C)', 'Max (°C)', 'Rain (mm)', 'Rain 1h (mm)', 'Rain 3h (mm)', 'Humidity (%)', 'Wind (m/s)']
                        st.dataframe(display_df, use_container_width=True)
                        
                        # Charts
                        st.markdown("### 📈 Historical Trends")
                        col1, col2 = st.columns(2)
                        with col1:
                            if 'rain' in df.columns:
                                st.bar_chart(df.set_index('date')['rain'])
                                st.caption("Historical Rainfall (mm)")
                        with col2:
                            if 'temperature' in df.columns:
                                st.line_chart(df.set_index('date')[['temperature', 'min_temp', 'max_temp']])
                                st.caption("Historical Temperature (°C)")
                        
                        # Summary statistics
                        st.markdown("### 📊 Summary Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Rainfall", f"{df['rain'].sum():.2f} mm")
                        with col2:
                            st.metric("Avg Rainfall/Day", f"{df['rain'].mean():.2f} mm")
                        with col3:
                            st.metric("Max Rainfall", f"{df['rain'].max():.2f} mm")
                        with col4:
                            st.metric("Avg Temperature", f"{df['temperature'].mean():.1f}°C")
                    
                    if history_range.get("warnings"):
                        st.warning("⚠️ Some data could not be fetched. Check warnings above.")
            except Exception as e:
                st.error(f"❌ Error fetching historical range: {e}")
    else:
        st.warning("⚠️ Could not find that location. Try a nearby city.")
