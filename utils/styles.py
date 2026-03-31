import streamlit as st

def apply_cyber_theme():
    st.markdown("""
    <style>
    .main { background-color: #050b14; }
    .stMetric { 
        background-color: rgba(15, 23, 42, 0.8); 
        padding: 20px; 
        border-radius: 10px; 
        border: 1px solid #00d2ff; 
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.15);
    }
    h1, h2, h3, h4, p { color: #e2e8f0 !important; }
    div[data-testid="stSidebar"] { background-color: rgba(10, 15, 30, 0.95); }
    .dataframe { border: 1px solid #00d2ff !important; }
    </style>
    """, unsafe_allow_html=True)
