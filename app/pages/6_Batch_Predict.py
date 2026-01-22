import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import io

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Batch Prediction", layout="wide")

st.title("📦 Batch Prediction")
st.markdown("Upload a CSV file with multiple soil samples for bulk predictions")

# File upload
uploaded_file = st.file_uploader(
    "Choose a CSV file",
    type=['csv'],
    help="CSV should contain columns: N, P, K, temperature, humidity, ph, rainfall, soil_type"
)

if uploaded_file is not None:
    try:
        # Preview uploaded file
        df = pd.read_csv(uploaded_file)
        st.markdown("### 📄 File Preview")
        st.dataframe(df.head(), use_container_width=True)
        
        # Check required columns
        required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_type']
        missing = [col for col in required_cols if col not in df.columns]
        
        if missing:
            st.error(f"❌ Missing required columns: {', '.join(missing)}")
            st.info(f"Required columns: {', '.join(required_cols)}")
        else:
            if st.button("🚀 Run Batch Prediction"):
                with st.spinner(f"⏳ Processing {len(df)} samples..."):
                    try:
                        # Prepare file for upload
                        file_bytes = uploaded_file.getvalue()
                        files = {"file": ("batch.csv", file_bytes, "text/csv")}
                        
                        res = requests.post(f"{API_BASE_URL}/batch-predict", files=files)
                        data = res.json()
                        
                        if "error" in data:
                            st.error(f"❌ Error: {data['error']}")
                        else:
                            results = data.get("results", [])
                            total = data.get("total_rows", 0)
                            successful = data.get("successful", 0)
                            
                            st.success(f"✅ Processed {successful}/{total} samples successfully!")
                            
                            # Display results
                            results_df = pd.DataFrame(results)
                            st.markdown("### 📊 Batch Prediction Results")
                            st.dataframe(results_df, use_container_width=True)
                            
                            # Summary statistics
                            if successful > 0:
                                st.markdown("### 📈 Summary")
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    avg_confidence = results_df['confidence'].mean() if 'confidence' in results_df.columns else 0
                                    st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
                                
                                with col2:
                                    avg_health = results_df['soil_health_score'].mean() if 'soil_health_score' in results_df.columns else 0
                                    st.metric("Avg Soil Health", f"{avg_health:.1f}")
                                
                                with col3:
                                    unique_crops = results_df['predicted_crop'].nunique() if 'predicted_crop' in results_df.columns else 0
                                    st.metric("Unique Crops", unique_crops)
                                
                                # Crop distribution
                                if 'predicted_crop' in results_df.columns:
                                    st.markdown("### 🌾 Crop Distribution")
                                    crop_counts = results_df['predicted_crop'].value_counts()
                                    st.bar_chart(crop_counts)
                                
                                # Download results
                                csv = results_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Results as CSV",
                                    data=csv,
                                    file_name="batch_predictions.csv",
                                    mime="text/csv"
                                )
                            
                    except Exception as e:
                        st.error(f"🚨 Batch prediction failed: {e}")
    
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

# Sample CSV template
with st.expander("📝 Sample CSV Template"):
    sample_data = {
        'N': [90, 85, 60],
        'P': [42, 58, 55],
        'K': [43, 41, 44],
        'temperature': [20.88, 21.77, 23.00],
        'humidity': [82.0, 80.3, 82.3],
        'ph': [6.5, 7.0, 7.8],
        'rainfall': [202.9, 226.7, 264.0],
        'soil_type': ['alluvial soil', 'black soil', 'red soil']
    }
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df)
    csv = sample_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Template",
        data=csv,
        file_name="batch_template.csv",
        mime="text/csv"
    )

