import streamlit as st

def apply_cyber_theme():
    st.markdown("""
    <style>
    /* 1. Fondo Titanio Profundo (Menos 'Gaming', más 'Data Center') */
    .main { 
        background-color: #0b0e14; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 2. Tabs Personalizadas (El cambio clave) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #161b22;
        border-radius: 8px 8px 0px 0px;
        color: #94a3b8;
        border: 1px solid #30363d;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #00d2ff !important;
        border-bottom: 2px solid #00d2ff !important;
    }

    /* 3. Tarjetas con menos brillo y más estructura */
    .titanium-card {
        background: #161b22;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #30363d;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .titanium-label {
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .titanium-value {
        font-size: 1.8rem;
        color: #f1f5f9;
        font-weight: 600;
    }
    .titanium-accent-value {
        font-size: 1.8rem;
        color: #38bdf8;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

def custom_metric_card(label, value, delta=None, delta_positive=True, is_accent=False, help_text=""):
    value_class = "titanium-accent-value" if is_accent else "titanium-value"
    st.markdown(f"""
    <div class="titanium-card" title="{help_text}">
        <div class="titanium-label">{label}</div>
        <div class="{value_class}">{value}</div>
        <div style="font-size:0.8rem; color:{'#4ade80' if delta_positive else '#f87171'}">{delta if delta else ''}</div>
    </div>
    """, unsafe_allow_html=True)
