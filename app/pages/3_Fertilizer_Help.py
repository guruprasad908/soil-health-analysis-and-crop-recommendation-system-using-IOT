import streamlit as st
from shared import render_header, render_footer

st.set_page_config(page_title="Fertilizer Help", layout="wide")

# 🔰 Header
render_header()

st.title("🧪 Fertilizer Help & Soil Enrichment Guide")

# Tabs
tab1, tab2, tab3 = st.tabs(["🌾 NPK Nutrients", "🌱 Organic & Bio-Fertilizers", "📋 Tips & Guide"])

# --- Tab 1: NPK Roles ---
with tab1:
    st.subheader("🌿 Role of Essential Nutrients")

    st.markdown("### 🟩 Nitrogen (N)")
    st.write("- Promotes leafy growth and green color.")
    st.write("- Deficiency: Yellowing of leaves, stunted growth.")
    st.write("- Sources: Urea, compost, manure, Rhizobium.")

    st.markdown("### 🟦 Phosphorus (P)")
    st.write("- Essential for root development and flowering.")
    st.write("- Deficiency: Purple/reddish leaves, poor flowering.")
    st.write("- Sources: Bone meal, rock phosphate, PSB bacteria.")

    st.markdown("### 🟧 Potassium (K)")
    st.write("- Enhances disease resistance and water regulation.")
    st.write("- Deficiency: Brown edges, weak stems.")
    st.write("- Sources: Wood ash, banana peel powder, potash.")

# --- Tab 2: Bio-Fertilizers ---
with tab2:
    st.subheader("🧬 Organic & Bio-Fertilizers")

    st.markdown("#### 🌱 Rhizobium")
    st.write("- Nitrogen fixer for legumes (e.g., soybeans, chickpeas).")

    st.markdown("#### 🌱 Azospirillum")
    st.write("- Associates with cereals like rice, wheat, maize.")

    st.markdown("#### 🌱 PSB (Phosphate Solubilizing Bacteria)")
    st.write("- Helps make phosphorus available in the soil.")

    st.markdown("#### ♻️ Other Organic Sources")
    st.write("- Vermicompost, green manure, neem cake, cow dung slurry.")

# --- Tab 3: General Tips ---
with tab3:
    st.subheader("📋 Fertilizer Application Tips")

    st.write("- Always test your soil before applying any fertilizer.")
    st.write("- Do not overuse chemical fertilizers — balance with organic inputs.")
    st.write("- Apply in split doses rather than all at once.")
    st.write("- Keep soil pH in check (ideal is 6.5 - 7.5).")

    

# 🔗 Footer
render_footer()
