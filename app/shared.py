import streamlit as st

def render_header(title="🌿 Soil Health & Crop Recommender"):
    st.markdown(f"""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #2E8B57;'>{title}</h1>
            <p style='font-size: 18px; color: gray;'>Empowering farmers with data-driven crop suggestions</p>
        </div>
        <hr>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background-color: #f9f9f9;
                padding: 10px;
                text-align: center;
                font-size: 14px;
                color: gray;
                z-index: 999;
            }
        </style>
        <div class="footer">
            Soil Health System | Built with ❤️ using Streamlit |
            <a href='https://github.com/guruprasad908' target='_blank'>GitHub</a>
        </div>
    """, unsafe_allow_html=True)
