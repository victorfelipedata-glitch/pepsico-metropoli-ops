import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- IMPORTAMOS NUESTROS PROPIOS MÓDULOS ---
from utils.styles import apply_cyber_theme
from utils.data_engine import load_hyper_data

# --- 1. SETUP CYBER-CORPORATIVO MAX ---
st.set_page_config(page_title="PepsiCo | Command Center MAX", layout="wide", initial_sidebar_state="expanded")

# --- 2. APLICAR ESTILOS Y CARGAR DATOS ---
apply_cyber_theme()
df = load_hyper_data()

# --- 3. PANEL HOLOGRÁFICO LATERAL ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/PepsiCo_logo.svg/1024px-PepsiCo_logo.svg.png", width=120)
st.sidebar.markdown("### 🛰️ Satélites Enlazados")

default_zonas = ['Naucalpan', 'Ecatepec', 'Iztapalapa', 'GAM', 'Cuauhtémoc', 'Atizapán', 'Tlalnepantla']
zona_sel = st.sidebar.multiselect("Nodos Metropolitanos:", options=list(df['Ubicación'].unique()), default=default_zonas)

prod_sel = st.sidebar.multiselect("Carga Comercial (SKUs):", options=list(df['Producto'].unique()), default=['Sabritas Original', 'Pepsi Black', 'Doritos Incógnita'])

# --- NUEVO: Rango Temporal ---
st.sidebar.markdown("### ⏱️ Rango Temporal")
min_date = df['Fecha'].min().date()
max_date = df['Fecha'].max().date()

date_range = st.sidebar.date_input(
    "Ventana de análisis:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Lógica de fechas (Streamlit devuelve 1 o 2 valores dependiendo de si el usuario ya hizo clic)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = date_range[0], date_range[0]

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtro Maestro Multivariable
df_f = df[
    (df['Ubicación'].isin(zona_sel)) & 
    (df['Producto'].isin(prod_sel)) &
    (df['Fecha'] >= start_date) & 
    (df['Fecha'] <= end_date)
]

# Validación de seguridad: Si el usuario filtra tanto que se queda sin datos
if df_f.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados. Amplía el rango temporal o selecciona otros nodos.")
    st.stop() # Esto detiene el código para que las gráficas no marquen error

# --- 4. HEADER Y KPIs ---
st.write("##") # Espacio extra para que no se corte el título
st.title("🌐 Centro de Comando Cuántico PepsiCo")
st.caption(f"Monitorización a Gran Escala | Escaneando {len(zona_sel)} nodos y {len(prod_sel)} SKUs")
st.divider()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Volumen Procesado (SKU)", f"{df_f['Ventas'].sum():,} u")
k2.metric("Saturación de Nodos", f"{len(zona_sel)} / 25", delta="Red Estable")
k3.metric("Pico Máximo Detectado", f"{df_f['Ventas'].max()} u", delta="Alerta Nivel 1" if df_f['Ventas'].max() > 150 else "Normal", delta_color="inverse")
k4.metric("Valor Est. Inventario", f"${df_f['Ventas'].sum() * 22.5:,.2f} MXN")

# --- 5. BLOQUE 1: MAPA Y RADAR MULTIVARIABLE ---
st.divider()
st.markdown("### 📍 Módulo Geoespacial y Multivariable")
c_map, c_radar = st.columns([1.5, 1])

with c_map:
    fig_map = px.scatter_mapbox(df_f.groupby('Ubicación', as_index=False).agg({'Ventas':'sum', 'lat':'first', 'lon':'first'}), 
                                lat='lat', lon='lon', size='Ventas', 
                                color='Ventas', color_continuous_scale='teal',
                                hover_name='Ubicación', zoom=9.5, mapbox_style="carto-darkmatter")
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_map, use_container_width=True)

with c_radar:
    categorias = ['Demanda Base', 'Penetración', 'Estabilidad', 'Margen Ops', 'Rotación']
    valores = [np.random.randint(70, 100) for _ in range(5)]
    fig_radar = go.Figure(data=go.Scatterpolar(r=valores, theta=categorias, fill='toself', fillcolor='rgba(0, 210, 255, 0.3)', line=dict(color='#00d2ff', width=3)))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='gray')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#00d2ff', size=12))
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 6. BLOQUE 2: TREEMAP MASIVO ---
st.divider()
st.markdown("### 🟦 Topografía de Mercado (Treemap de Dominancia)")
st.write("Visualiza la cuota de mercado por zona y producto. Los cuadros más grandes representan mayor volumen de desplazamiento.")

fig_tree = px.treemap(df_f, path=[px.Constant("Valle de México"), 'Ubicación', 'Producto'], 
                      values='Ventas', color='Ventas', color_continuous_scale='Blues')
fig_tree.update_layout(margin=dict(t=20, l=0, r=0, b=0), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
st.plotly_chart(fig_tree, use_container_width=True)

# --- 7. BLOQUE 3: ANÁLISIS TEMPORAL Y ANOMALÍAS ---
st.divider()
st.markdown("### ⏱️ Análisis Temporal y Detección de Shocks")
c_heat, c_anom = st.columns([1, 1.5])

with c_heat:
    st.markdown("#### Matriz de Demanda por Día")
    orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    df_heat = df_f.groupby('Dia_Semana')['Ventas'].mean().reindex(orden_dias).reset_index()
    fig_heat = px.density_heatmap(df_f, x='Dia_Semana', y='Producto', z='Ventas', histfunc='avg', 
                                  color_continuous_scale='tealgrn', category_orders={'Dia_Semana': orden_dias})
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'))
    st.plotly_chart(fig_heat, use_container_width=True)

with c_anom:
    st.markdown("#### 🤖 Escáner de Fracturas de Inventario (IA)")
    df_g = df_f.groupby('Fecha')['Ventas'].sum().reset_index()
    media, desviacion = df_g['Ventas'].mean(), df_g['Ventas'].std()
    df_g['Anomalia'] = np.where(abs(df_g['Ventas'] - media) > (2 * desviacion), True, False)
    
    fig_anom = go.Figure()
    fig_anom.add_trace(go.Scatter(x=df_g['Fecha'], y=df_g['Ventas'], mode='lines', name='Flujo Normal', line=dict(color='#00d2ff', width=2)))
    anomalias = df_g[df_g['Anomalia'] == True]
    fig_anom.add_trace(go.Scatter(x=anomalias['Fecha'], y=anomalias['Ventas'], mode='markers', name='Shock de Mercado', marker=dict(color='#ff003c', size=12, symbol='x')))
    fig_anom.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), hovermode="x unified")
    st.plotly_chart(fig_anom, use_container_width=True)

# --- 8. BLOQUE 4: TERMINAL LOGÍSTICA Y EXPORTACIÓN ---
st.divider()
st.markdown("### 📋 Terminal de Acción Logística")

resumen = df_f.groupby(['Ubicación', 'Producto']).agg(
    Ventas_Totales=('Ventas', 'sum'),
    Promedio_Diario=('Ventas', 'mean')
).reset_index()

resumen['Promedio_Diario'] = resumen['Promedio_Diario'].round(2)
resumen['Estatus'] = np.where(resumen['Promedio_Diario'] < 30, '🔴 Riesgo Desabasto', '🟢 Óptimo')
resumen['Acción Sugerida'] = np.where(resumen['Estatus'] == '🔴 Riesgo Desabasto', 'Aumentar Frecuencia', 'Mantener Surtido')

c_tabla, c_export = st.columns([3, 1])
with c_tabla:
    # Usamos pandas styler para colorear el semáforo
    st.dataframe(resumen.style.map(lambda x: 'color: #ff4b4b' if '🔴' in str(x) else ('color: #00e676' if '🟢' in str(x) else ''), subset=['Estatus']), use_container_width=True)

with c_export:
    st.markdown("#### Exportar Base de Datos")
    st.write("Descarga los datos filtrados para integrar con SAP o Excel.")
    csv = resumen.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte CSV",
        data=csv,
        file_name='pepsico_reporte_metropolitano.csv',
        mime='text/csv',
    )
    st.info("Formato listo para lectura de macros en Power Query y SQL.")

# --- FOOTER CLASIFICADO ---
st.divider()
st.caption("© 2026 PepsiCo Intelligence System | Data Analyst Victor Antonio")
