

import streamlit as st
from shared import render_header, render_footer
import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


st.set_page_config(page_title="Soil Crop Recommender", layout="wide")

# Inject CSS for card styling and layout
st.markdown("""
<style>
    .hero {
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 1rem;
    }
    .hero h1 {
        font-size: 2.8rem;
        margin-bottom: 0.3rem;
    }
    .hero p {
        font-size: 1.1rem;
        color: #aaa;
    }
    .feature-card {
        background-color: #1e1e1e;
        border-radius: 12px;
        border: 1px solid #333;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        border-color: #00cc88;
    }
    .feature-card h3 {
        color: white;
        margin-top: 0.8rem;
    }
    .feature-card p {
        color: #ccc;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)



# 🌟 Hero Section
st.markdown("""
<div class='hero'>
    <h1>🌾 Soil Health & Crop Recommendation System</h1>
    <p>Empowering farmers with AI-driven decisions for better yield, soil care, and climate insights.</p>
</div>
""", unsafe_allow_html=True)

# 🚀 Feature Cards Section
st.markdown("## 🔍 Explore Features")

# First row - Core features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div style="font-size: 40px;">🌦️</div>
        <h3>Live Weather Insights</h3>
        <p>Check real-time weather and 5-day forecasts to adapt your farming decisions.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Weather.py", label="🌦️ Check Weather → ")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div style="font-size: 40px;">🌱</div>
        <h3>Smart Crop Prediction</h3>
        <p>Get crop recommendations with soil health scoring and model selection.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_predict.py", label="🌱 Predict Crops →")
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div style="font-size: 40px;">🧪</div>
        <h3>Fertilizer Guidance</h3>
        <p>Understand NPK roles, bio-fertilizers, and soil treatment suggestions.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Fertilizer_Help.py", label="🧪 Fertilizer Help →")
    st.markdown("</div>", unsafe_allow_html=True)

# Second row - Advanced features
st.markdown("## 🚀 Advanced Features")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class='feature-card'>
        <div style="font-size: 40px;">🔄</div>
        <h3>Model Comparison</h3>
        <p>Compare predictions from all ML models side-by-side for better insights.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Model_Comparison.py", label="🔄 Compare Models →")
    st.markdown("</div>", unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class='feature-card'>
        <div style="font-size: 40px;">📊</div>
        <h3>Prediction History</h3>
        <p>Track your predictions over time and monitor soil health trends.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_History.py", label="📊 View History →")
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class='feature-card'>
        <div style="font-size: 40px;">📦</div>
        <h3>Batch Prediction</h3>
        <p>Upload CSV file for bulk predictions on multiple soil samples.</p>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_Batch_Predict.py", label="📦 Batch Predict →")
    st.markdown("</div>", unsafe_allow_html=True)


# 🔗 Footer
render_footer()
