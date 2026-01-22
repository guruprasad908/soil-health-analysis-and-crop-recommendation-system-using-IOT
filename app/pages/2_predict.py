import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Crop Prediction", layout="wide")

# 👉 Styling for consistency
st.markdown("""
<style>
    .form-container {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #333;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
    }
    .result-box {
        background-color: #262626;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 1px solid #444;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌱 Smart Crop Prediction")

# Fetch available models
try:
    models_response = requests.get(f"{API_BASE_URL}/models")
    if models_response.status_code == 200:
        models_data = models_response.json()
        available_models = models_data.get("available_models", ["Stacking Classifier"])
        model_details = models_data.get("model_details", {})
    else:
        available_models = ["Stacking Classifier", "Random Forest", "Gradient Boosting", "Decision Tree"]
        model_details = {}
except:
    available_models = ["Stacking Classifier", "Random Forest", "Gradient Boosting", "Decision Tree"]
    model_details = {}

# 🌿 Input form
with st.form("prediction_form"):
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.subheader("📋 Enter Soil & Weather Details")
    
    # Model Selection
    st.markdown("### 🤖 Select ML Model")
    selected_model = st.selectbox(
        "Choose prediction model:",
        options=available_models,
        index=0,
        help="Select the machine learning model to use for crop prediction"
    )
    
    # Show model description if available
    if selected_model in model_details:
        model_info = model_details[selected_model]
        st.info(f"📊 **{model_info.get('type', 'Model')}**: {model_info.get('description', '')}")

    st.markdown("---")

    farmer_name = st.text_input("👨‍🌾 Farmer Name")
    phone = st.text_input("📞 Phone Number")
    location = st.text_input("📍 Location")
    land_size = st.number_input("🌾 Land Size (acres)", min_value=0.1, format="%.2f")

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

    st.markdown("</div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("📤 Predict Crop")

# 🔍 Process submission
if submitted:
    # Simple validation
    if not farmer_name or not phone or not location:
        st.error("❗ Please fill out all required fields.")
    else:
        with st.spinner("⏳ Predicting the best crop..."):
            try:
                payload = {
                    "farmer_name": farmer_name,
                    "phone": phone,
                    "location": location,
                    "land_size": land_size,
                    "N": N, "P": P, "K": K,
                    "ph": ph,
                    "temperature": temperature,
                    "humidity": humidity,
                    "rainfall": rainfall,
                    "soil_type": soil_type,
                    "model_name": selected_model
                }

                res = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=30)
                data = res.json()

                if "error" in data or "detail" in data:
                    error_msg = data.get("error") or data.get("detail", "Unknown error")
                    st.error(f"❌ Error: {error_msg}")
                else:
                    st.success("✅ Prediction complete!")

                    # Display warnings if any
                    if data.get("warnings"):
                        for warning in data["warnings"]:
                            st.warning(warning)

                    with st.container():
                        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
                        
                        # Main prediction with confidence
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.markdown(f"### 🌾 Recommended Crop: **{data['predicted_crop'].title()}**")
                            # Show which model was used
                            model_used = data.get("model_used", "Stacking Classifier")
                            st.caption(f"🤖 Model: {model_used}")
                        with col2:
                            confidence = data.get("confidence", 0)
                            # Color code confidence
                            if confidence >= 80:
                                conf_color = "🟢"
                            elif confidence >= 60:
                                conf_color = "🟡"
                            else:
                                conf_color = "🟠"
                            st.metric("Confidence", f"{conf_color} {confidence:.1f}%")

                        # Top alternatives
                        if data.get("top_alternatives"):
                            st.markdown("#### 🔄 Alternative Crop Options")
                            alt_cols = st.columns(len(data["top_alternatives"]))
                            for idx, alt in enumerate(data["top_alternatives"]):
                                with alt_cols[idx]:
                                    st.metric(
                                        f"{alt['crop'].title()}",
                                        f"{alt['confidence']:.1f}%",
                                        delta=f"{alt['confidence'] - confidence:.1f}%"
                                    )

                        st.markdown("---")
                        
                        # Soil Health Score
                        if data.get("soil_health"):
                            soil_health = data["soil_health"]
                            st.markdown("#### 🏥 Soil Health Score")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                score = soil_health.get("overall_score", 0)
                                category = soil_health.get("category", "Unknown")
                                color = soil_health.get("color", "gray")
                                
                                # Color-coded metric
                                if score >= 80:
                                    st.metric("Overall Score", f"{score:.1f}/100", "Excellent", delta_color="normal")
                                elif score >= 65:
                                    st.metric("Overall Score", f"{score:.1f}/100", "Good", delta_color="normal")
                                elif score >= 50:
                                    st.metric("Overall Score", f"{score:.1f}/100", "Fair", delta_color="off")
                                else:
                                    st.metric("Overall Score", f"{score:.1f}/100", "Poor", delta_color="inverse")
                            
                            with col2:
                                st.markdown(f"**Category:** {category}")
                            
                            with col3:
                                if soil_health.get("recommendations"):
                                    st.markdown("**Recommendations:**")
                                    for rec in soil_health["recommendations"][:2]:
                                        st.caption(rec)
                            
                            # Breakdown chart
                            if soil_health.get("breakdown"):
                                st.markdown("**Score Breakdown:**")
                                breakdown = soil_health["breakdown"]
                                breakdown_df = pd.DataFrame({
                                    "Component": list(breakdown.keys()),
                                    "Score": list(breakdown.values())
                                })
                                st.bar_chart(breakdown_df.set_index("Component"))
                        
                        st.markdown("---")

                        # Soil Treatment
                        st.markdown("#### 🧪 Soil Treatment Recommendations")
                        soil_treatment = data.get("soil_treatment", [])
                        if soil_treatment:
                            for suggestion in soil_treatment:
                                # Format suggestions nicely
                                if suggestion.startswith("✅"):
                                    st.success(suggestion)
                                elif suggestion.startswith("⚠️"):
                                    st.warning(suggestion)
                                else:
                                    st.info(suggestion)
                        else:
                            st.info("No specific soil treatment recommendations.")

                        st.markdown("---")
                        
                        # NPK Visualization
                        st.markdown("#### 📊 Soil NPK Levels")
                        npk_data = pd.DataFrame({
                            "Nutrient": ["Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"],
                            "Value (mg/kg)": [N, P, K]
                        })
                        st.bar_chart(npk_data.set_index("Nutrient"))
                        
                        # NPK comparison with ideal
                        st.markdown("**Current vs Ideal NPK:**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("N", f"{N} mg/kg", f"Range: 50-100")
                        with col2:
                            st.metric("P", f"{P} mg/kg", f"Range: 30-60")
                        with col3:
                            st.metric("K", f"{K} mg/kg", f"Range: 30-80")
                        
                        st.markdown("---")

                        # Fertilizer Estimate
                        st.markdown("#### 📦 Fertilizer Recommendations")
                        fertilizer_estimate = data.get("fertilizer_estimate", "")
                        if fertilizer_estimate:
                            # Display as formatted text
                            st.markdown(f"<div style='background-color: #1a1a1a; padding: 1rem; border-radius: 5px; font-family: monospace; white-space: pre-wrap;'>{fertilizer_estimate}</div>", unsafe_allow_html=True)
                        else:
                            st.info("Fertilizer recommendations not available for this crop.")

                        st.markdown("---")

                        # Download PDF
                        if data.get("pdf_url"):
                            st.markdown("#### 📄 Report Download")
                            st.markdown(f"""
                            <a href="{API_BASE_URL}{data['pdf_url']}" target="_blank" style="
                                display: inline-block;
                                padding: 0.5rem 1rem;
                                background-color: #00cc88;
                                color: white;
                                text-decoration: none;
                                border-radius: 5px;
                                font-weight: bold;
                            ">
                                📥 Download PDF Report
                            </a>
                            """, unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"🚨 Failed to connect to API: {e}")
                st.error(f"🔧 Please check if the FastAPI server is running on {API_BASE_URL}")
