import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Prediction History", layout="wide")

st.title("📊 Prediction History")
st.markdown("View historical predictions and track soil health over time")

# Search form
with st.form("history_form"):
    col1, col2 = st.columns(2)
    with col1:
        farmer_name = st.text_input("👨‍🌾 Farmer Name (optional)")
    with col2:
        phone = st.text_input("📞 Phone Number (optional)")
    
    limit = st.slider("Number of records", 5, 50, 10)
    submitted = st.form_submit_button("🔍 Search History")

if submitted or st.session_state.get("show_history", False):
    with st.spinner("⏳ Loading history..."):
        try:
            params = {"limit": limit}
            if farmer_name:
                params["farmer_name"] = farmer_name
            if phone:
                params["phone"] = phone
            
            res = requests.get(f"{API_BASE_URL}/history", params=params)
            data = res.json()
            
            if "error" in data:
                st.error(f"❌ Error: {data['error']}")
            else:
                predictions = data.get("predictions", [])
                count = data.get("count", 0)
                
                if count > 0:
                    st.success(f"✅ Found {count} prediction(s)")
                    
                    # Convert to DataFrame
                    df = pd.DataFrame(predictions)
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    df = df.sort_values('timestamp', ascending=False)
                    
                    # Display metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Predictions", count)
                    with col2:
                        avg_confidence = df['confidence'].mean() if 'confidence' in df.columns else 0
                        st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
                    with col3:
                        avg_health = df['soil_health_score'].mean() if 'soil_health_score' in df.columns else 0
                        st.metric("Avg Soil Health", f"{avg_health:.1f}")
                    with col4:
                        unique_crops = df['predicted_crop'].nunique() if 'predicted_crop' in df.columns else 0
                        st.metric("Unique Crops", unique_crops)
                    
                    # Display table
                    st.markdown("### 📋 Prediction History")
                    st.dataframe(df, use_container_width=True)
                    
                    # Charts
                    if len(df) > 1:
                        st.markdown("### 📈 Trends")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            if 'soil_health_score' in df.columns:
                                st.line_chart(df.set_index('timestamp')['soil_health_score'])
                                st.caption("Soil Health Score Over Time")
                        
                        with col2:
                            if 'confidence' in df.columns:
                                st.line_chart(df.set_index('timestamp')['confidence'])
                                st.caption("Prediction Confidence Over Time")
                    
                    # Crop distribution
                    if 'predicted_crop' in df.columns:
                        st.markdown("### 🌾 Crop Distribution")
                        crop_counts = df['predicted_crop'].value_counts()
                        st.bar_chart(crop_counts)
                else:
                    st.info("No predictions found. Make some predictions first!")
                    
        except Exception as e:
            st.error(f"🚨 Failed to load history: {e}")

