import streamlit as st

def apply_cyber_theme():
    st.markdown("""
    <style>
    /* 1. Fondo Principal y Tipografía General */
    .main { 
        background-color: #0d1117; /* Gris titanio muy oscuro */
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, p { 
        color: #e2e8f0 !important; 
        font-weight: 300;
    }
    
    /* 2. Barra Lateral Refinada */
    [data-testid="stSidebar"] { 
        background-color: #161b22; /* Ligeramente más claro que el fondo para dar profundidad */
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 1.1rem;
        color: #00d2ff !important;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* 3. Limpieza de los Chips de Multiselect (para que no sean tan rojos) */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #30363d !important;
        border: 1px solid #00d2ff !important;
        color: #e2e8f0 !important;
    }

    /* 4. Tarjetas de Métricas Personalizadas (Custom Cards) */
    .titanium-card {
        background: rgba(30, 41, 59, 0.6); /* Efecto Glassmorphism */
        backdrop-filter: blur(5px);
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(226, 232, 240, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
    }
    .titanium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 210, 255, 0.1);
        border: 1px solid rgba(0, 210, 255, 0.3);
    }
    .titanium-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 8px;
    }
    .titanium-value {
        font-size: 2.2rem;
        color: #e2e8f0;
        font-weight: 700;
    }
    .titanium-accent-value {
        font-size: 2.2rem;
        color: #00d2ff; /* Usamos cian para valores que brillan */
        font-weight: 700;
    }
    .titanium-delta {
        font-size: 0.9rem;
        margin-top: 4px;
    }
    .delta-positive { color: #00e676; }
    .delta-negative { color: #ff4b4b; }

    /* 5. Contenedor de Encabezado (Title Banner) */
    .header-banner {
        background: radial-gradient(circle at center, rgba(30, 41, 59, 0.7) 0%, rgba(13, 17, 23, 0) 70%);
        padding: 40px 0;
        border-radius: 15px;
        margin-bottom: 30px;
    }
    
    /* 6. Mejoras generales de Plotly y DF */
    .dataframe { 
        border: 1px solid rgba(0, 210, 255, 0.2) !important; 
        background-color: #161b22 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Nueva Función auxiliar para crear las tarjetas
def custom_metric_card(label, value, delta=None, delta_positive=True, is_accent=False, help_text=""):
    value_class = "titanium-accent-value" if is_accent else "titanium-value"
    
    delta_html = ""
    if delta:
        delta_class = "delta-positive" if delta_positive else "delta-negative"
        delta_html = f'<div class="titanium-delta {delta_class}">{delta}</div>'
    
    # El parámetro 'title' en el div crea un tooltip nativo sencillo
    st.markdown(f"""
    <div class="titanium-card" title="{help_text}">
        <div class="titanium-label">{label} ℹ️</div>
        <div class="{value_class}">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)
