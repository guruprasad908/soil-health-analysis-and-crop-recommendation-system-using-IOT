import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Model Comparison", layout="wide")

st.title("🔄 Model Comparison")
st.markdown("Compare predictions from all available ML models side-by-side")

# Input form
with st.form("comparison_form"):
    st.subheader("📋 Enter Soil & Weather Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.slider("Nitrogen (N)", 0, 140, 50)
        P = st.slider("Phosphorus (P)", 0, 140, 50)
    with col2:
        K = st.slider("Potassium (K)", 0, 140, 50)
        ph = st.slider("Soil pH", 3.5, 9.0, 6.5)
    with col3:
        temperature = st.slider("🌡 Temperature (°C)", 5.0, 45.0, 25.0)
        humidity = st.slider("💧 Humidity (%)", 0.0, 100.0, 60.0)
    
    rainfall = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, format="%.2f")
    soil_type = st.selectbox("🧪 Soil Type", [
        "alluvial soil", "black soil", "red soil",
        "laterite soil", "sandy soil", "peaty soil"
    ])
    
    submitted = st.form_submit_button("🔄 Compare All Models")

if submitted:
    with st.spinner("⏳ Comparing models..."):
        try:
            payload = {
                "farmer_name": "Comparison Test",
                "phone": "1234567890",
                "location": "Test",
                "land_size": 1.0,
                "N": N, "P": P, "K": K,
                "ph": ph,
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall,
                "soil_type": soil_type,
                "model_name": "Random Forest"
            }
            
            res = requests.post(f"{API_BASE_URL}/compare-models", json=payload)
            data = res.json()
            
            if "error" in data or "detail" in data:
                st.error(f"❌ Error: {data.get('error') or data.get('detail')}")
            else:
                st.success("✅ Comparison complete!")
                
                # Display comparison table
                comparisons = data.get("comparisons", [])
                if comparisons:
                    df = pd.DataFrame(comparisons)
                    
                    # Highlight best confidence
                    st.markdown("### 📊 Model Comparison Results")
                    
                    # Create comparison cards
                    cols = st.columns(len(comparisons))
                    for idx, comp in enumerate(comparisons):
                        with cols[idx]:
                            if "error" not in comp:
                                st.metric(
                                    comp["model"],
                                    comp["predicted_crop"].title(),
                                    f"{comp['confidence']:.1f}%"
                                )
                            else:
                                st.error(f"{comp['model']}: Error")
                    
                    # Detailed table
                    st.markdown("### 📋 Detailed Comparison")
                    st.dataframe(df, use_container_width=True)
                    
                    # Find consensus
                    if len(comparisons) > 1:
                        crops = [c["predicted_crop"] for c in comparisons if "error" not in c]
                        if crops:
                            most_common = max(set(crops), key=crops.count)
                            st.info(f"🎯 **Consensus Prediction**: {most_common.title()} (appears in {crops.count(most_common)}/{len(crops)} models)")
                
        except Exception as e:
            st.error(f"🚨 Failed to compare models: {e}")

