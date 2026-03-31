import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.styles import apply_cyber_theme, custom_metric_card
from utils.data_engine import load_hyper_data

# --- 1. SETUP ---
st.set_page_config(page_title="PepsiCo | Inteligencia de Mercado", layout="wide", initial_sidebar_state="expanded")
apply_cyber_theme()
df = load_hyper_data()

# --- 2. BARRA LATERAL (Filtros + SIMULADOR + TOOLTIPS) ---
st.sidebar.markdown("# 🔱 Filtros de Red")
st.sidebar.write("Configura la vista de operaciones.")

with st.sidebar.expander("📍 Nodos Metropolitanos", expanded=True):
    zona_sel = st.multiselect("Nodos:", options=list(df['Ubicación'].unique()), default=['Naucalpan', 'Ecatepec', 'Iztapalapa', 'GAM'], help="Selecciona las zonas geográficas que deseas monitorear.")

with st.sidebar.expander("🥤 Carga Comercial (SKUs)", expanded=True):
    prod_sel = st.multiselect("SKUs:", options=list(df['Producto'].unique()), default=['Sabritas Original', 'Pepsi Black'], help="Selecciona los productos específicos para analizar su desplazamiento.")

with st.sidebar.expander("⏱️ Ventana de Análisis", expanded=True):
    date_range = st.date_input("Rango:", value=(df['Fecha'].min(), df['Fecha'].max()), help="Define el periodo de tiempo para el cálculo de métricas e histórico.")

# --- PUNTO 1: EL SIMULADOR DE ESCENARIOS ---
st.sidebar.divider()
st.sidebar.markdown("### 🧪 Simulador de Escenarios")
st.sidebar.write("Ajusta la demanda proyectada para prever shocks.")
factor_sim = st.sidebar.slider("Incremento de Demanda (%)", -50, 100, 0, help="Simula un evento (ej. Super Bowl o contingencia) aumentando o disminuyendo las ventas base.")

# Aplicación de filtros y lógica de simulación
start_date, end_date = date_range if len(date_range) == 2 else (date_range[0], date_range[0])
df_f = df[(df['Ubicación'].isin(zona_sel)) & (df['Producto'].isin(prod_sel)) & (df['Fecha'] >= pd.to_datetime(start_date)) & (df['Fecha'] <= pd.to_datetime(end_date))].copy()

# El cálculo matemático detrás de escenas
df_f['Ventas'] = (df_f['Ventas'] * (1 + factor_sim / 100)).astype(int)

if df_f.empty:
    st.warning("⚠️ Sin datos. Ajusta los filtros.")
    st.stop()

# --- 3. ENCABEZADO E INSIGHTS ---
h_logo, h_title = st.columns([1, 5])
with h_logo: st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/PepsiCo_logo.svg/1024px-PepsiCo_logo.svg.png", width=100)
with h_title:
    st.markdown(f"""<h1 style='margin-bottom:0;'>Centro de Comando PepsiCo</h1>
    <p style='color:#94a3b8;'>Monitorización de Inventario y Demanda | {start_date.strftime('%d %b')} - {end_date.strftime('%d %b')}</p>""", unsafe_allow_html=True)

# --- PUNTO 2: INSIGHTS TRADUCIDOS (TEXTO DIGERIBLE) ---
st.info("💡 **Análisis del Sistema:** " + 
    (f"Se observa un incremento crítico del {factor_sim}% sobre la demanda base. " if factor_sim > 20 else "") +
    f"El producto con mayor rotación actual es **{df_f.groupby('Producto')['Ventas'].sum().idxmax()}**. " +
    f"Se recomienda reforzar la logística en **{df_f.groupby('Ubicación')['Ventas'].sum().idxmax()}** debido al volumen proyectado.")

st.divider()

# --- 4. KPIs (CON TOOLTIPS) ---
k1, k2, k3, k4 = st.columns(4)
vol_sum = df_f['Ventas'].sum()
with k1: custom_metric_card("Volumen Total", f"{vol_sum:,} u", help_text="Suma total de unidades desplazadas en el periodo y zonas seleccionadas.")
with k2: custom_metric_card("Nodos Activos", f"{len(zona_sel)} / 25", delta="📡 Conexión Estable", help_text="Cantidad de centros de distribución o zonas activas bajo monitoreo.")
with k3: custom_metric_card("Pico de Demanda", f"{df_f['Ventas'].max()} u", is_accent=True, help_text="El valor de venta individual más alto detectado en un solo registro.")
with k4: custom_metric_card("Inventario Est.", f"${vol_sum * 22.5:,.0f}", help_text="Valorización aproximada del inventario en tránsito basada en el volumen actual.")

# --- 5. VISUALIZACIONES ---
paleta_unificada = ['#161b22', '#1e293b', '#007a99', '#00d2ff']

st.divider()
c_map, c_radar = st.columns([2, 1])

with c_map:
    st.markdown("### 📍 Distribución Espacial", help="Cada punto representa un nodo. El tamaño es proporcional a las ventas.")
    fig_map = px.scatter_mapbox(df_f.groupby('Ubicación', as_index=False).agg({'Ventas':'sum', 'lat':'first', 'lon':'first'}), 
                                lat='lat', lon='lon', size='Ventas', color='Ventas', color_continuous_scale=paleta_unificada,
                                zoom=9, mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

with c_radar:
    st.markdown("### 🕸️ Eficiencia de Red", help="Análisis de 5 ejes para medir la salud operativa de los nodos seleccionados.")
    fig_radar = go.Figure(data=go.Scatterpolar(r=[np.random.randint(70, 100) for _ in range(5)], theta=['Demanda', 'Penetración', 'Estabilidad', 'Margen', 'Rotación'], fill='toself', fillcolor='rgba(0, 210, 255, 0.15)', line=dict(color='#00d2ff', width=2)))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='gray')), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=10))
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. TREEMAP E HISTÓRICO ---
st.divider()
st.markdown("### 🟦 Dominancia de Mercado", help="Jerarquía de ventas por zona (cuadros grandes) y producto (cuadros internos).")
fig_tree = px.treemap(df_f, path=[px.Constant("Valle de México"), 'Ubicación', 'Producto'], values='Ventas', color='Ventas', color_continuous_scale=paleta_unificada)
fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0'))
fig_tree.update_traces(marker=dict(line=dict(color='#0d1117', width=2)), root_color="#0d1117")
st.plotly_chart(fig_tree, use_container_width=True)

# Footer
st.sidebar.caption(f"Operando en: {st.session_state.get('location', 'Zona Central')}")
