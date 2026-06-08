import streamlit as st

def apply_custom_ui():
    st.markdown("""
    <style>

    .stApp {
        background-color: #0E1117;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #2a2a2a;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB !important;
    }

    .card {
        background-color: #1C1F26;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }

    h1, h2, h3 {
        color: #E5E7EB;
    }

    input, select, textarea {
        background-color: #111827 !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid #2a2a2a !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #4CAF50, #00c853);
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True)