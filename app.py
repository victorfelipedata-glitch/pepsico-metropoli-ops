import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- IMPORTAMOS NUESTROS PROPIOS MÓDULOS ---
# Fíjate que ahora importamos 'custom_metric_card'
from utils.styles import apply_cyber_theme, custom_metric_card
from utils.data_engine import load_hyper_data

# --- 1. SETUP CYBER-CORPORATIVO MAX ---
st.set_page_config(page_title="PepsiCo | Command Center MAX", layout="wide", initial_sidebar_state="expanded")

# --- 2. APLICAR ESTILOS Y CARGAR DATOS ---
apply_cyber_theme()
df = load_hyper_data()

# --- 3. PANEL HOLOGRÁFICO LATERAL (Refinado y Organizado) ---
st.sidebar.markdown("# 🔱 Filtros Titanium")
st.sidebar.write("Gestiona la monitorización desde la red central.")
st.sidebar.divider()

# Usamos expanders para limpiar la vista
with st.sidebar.expander("📍 Nodos Metropolitanos", expanded=True):
    default_zonas = ['Naucalpan', 'Ecatepec', 'Iztapalapa', 'GAM', 'Cuauhtémoc', 'Atizapán', 'Tlalnepantla']
    zona_sel = st.multiselect("Seleccionar Nodos:", options=list(df['Ubicación'].unique()), default=default_zonas, label_visibility="collapsed")

with st.sidebar.expander("🥤 Carga Comercial (SKUs)", expanded=True):
    prod_sel = st.multiselect("Seleccionar SKUs:", options=list(df['Producto'].unique()), default=['Sabritas Original', 'Pepsi Black', 'Doritos Incógnita'], label_visibility="collapsed")

with st.sidebar.expander("⏱️ Ventana de Análisis", expanded=True):
    min_date = df['Fecha'].min().date()
    max_date = df['Fecha'].max().date()
    date_range = st.date_input("Rango temporal:", value=(min_date, max_date), min_value=min_date, max_value=max_date, label_visibility="collapsed")

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

# Validación de seguridad
if df_f.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados. Amplía el rango o selecciona otros nodos.")
    st.stop()

# Espaciado extra en sidebar
st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.sidebar.caption("© 2026 PepsiCo Intelligence | v1.0 Titanium")


# --- 4. SECCIÓN 0: ENCABEZADO CENTRAL PROFESIONAL ---
with st.container():
    h_logo, h_title, h_stats = st.columns([1, 3, 1])
    
    with h_logo:
        # Logo centrado arriba
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/PepsiCo_logo.svg/1024px-PepsiCo_logo.svg.png", width=120)
    
    with h_title:
        # Título sofisticado
        st.markdown("""
        <div style="text-align: center;">
            <h1 style="margin-bottom: 0px; font-weight: 700;">COMMAND CENTER TITANIUM</h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin-top: 5px;">Sistema de Monitorización de Operaciones | Valle de México</p>
        </div>
        """, unsafe_allow_html=True)

    with h_stats:
        # Una pequeña estadística rápida
        st.caption(f"Filtros Activos:<br>**{len(zona_sel)}** Nodos<br>**{len(prod_sel)}** SKUs", unsafe_allow_html=True)
st.divider()


# --- 5. BLOQUE DE KPIs: USANDO TARJETAS PERSONALIZADAS ---
st.markdown("### 📊 Indicadores Clave de Red")
k1, k2, k3, k4 = st.columns(4)

vol_sum = df_f['Ventas'].sum()
with k1:
    # Card 1: Volumen total
    custom_metric_card("Volumen Total", f"{vol_sum:,} u", delta=f"{len(df_f)} registros procesados", is_accent=False)

nodos_sat = len(zona_sel)
with k2:
    # Card 2: Nodos (con delta de estatus)
    custom_metric_card("Nodos Activos", f"{nodos_sat} / 25", delta="📡 Red Central Estable", delta_positive=True, is_accent=False)

pico_max = df_f['Ventas'].max()
with k3:
    # Card 3: Pico Máximo Detectado (Usamos el acento cian aquí)
    custom_metric_card("Pico de Demanda", f"{pico_max} u", delta="⚠️ Alerta Nivel 1 activa" if pico_max > 150 else "⚡ Normal", delta_positive=pico_max <= 150, is_accent=True)

inventario_est = vol_sum * 22.5
with k4:
    # Card 4: Inventario (con delta de divisa)
    custom_metric_card("Inventario Est.", f"${inventario_est:,.0f}", delta="Pesos Mexicanos (MXN)", is_accent=False)


# --- 6. BLOQUE 1: MAPA Y RADAR MULTIVARIABLE (Mejorando contenedores y márgenes) ---
st.divider()
st.markdown("### 📍 Módulo Geoespacial y Multivariable")
c_map, c_radar = st.columns([2, 1])

with c_map:
    st.write("Visualización espacial de nodos y volumen de ventas.")
    fig_map = px.scatter_mapbox(df_f.groupby('Ubicación', as_index=False).agg({'Ventas':'sum', 'lat':'first', 'lon':'first'}), 
                                lat='lat', lon='lon', size='Ventas', 
                                color='Ventas', color_continuous_scale='teal',
                                hover_name='Ubicación', zoom=9.2, mapbox_style="carto-darkmatter")
    # Tweakmargins y colores de Plotly para que no resalten
    fig_map.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        coloraxis_colorbar=dict(title=dict(text='Ventas', font=dict(color='white')), tickfont=dict(color='white'))
    )
    st.plotly_chart(fig_map, use_container_width=True)

with c_radar:
    st.write("Análisis Multivariable de Eficiencia.")
    categorias = ['Demanda Base', 'Penetración', 'Estabilidad', 'Margen Ops', 'Rotación']
    valores = [np.random.randint(70, 100) for _ in range(5)]
    fig_radar = go.Figure(data=go.Scatterpolar(r=valores, theta=categorias, fill='toself', fillcolor='rgba(0, 210, 255, 0.1)', line=dict(color='#00d2ff', width=2)))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='gray')), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=11))
    st.plotly_chart(fig_radar, use_container_width=True)


# --- 7. BLOQUE 2: TREEMAP MASIVO (Refinado) ---
st.divider()
st.markdown("### 🟦 Topografía de Mercado (Dominancia)")
st.write("Cuota de mercado por zona y SKU (Treemap). Los cuadros mayores indican mayor volumen.")

fig_tree = px.treemap(df_f, path=[px.Constant("Valle de México"), 'Ubicación', 'Producto'], 
                      values='Ventas', color='Ventas', color_continuous_scale='Blues')
fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=11))
st.plotly_chart(fig_tree, use_container_width=True)


# --- 8. BLOQUE 3: ANÁLISIS TEMPORAL Y ANOMALÍAS (Refinado) ---
st.divider()
st.markdown("### ⏱️ Análisis de Series Temporales y Detección de Shocks")
c_heat, c_anom = st.columns([1, 1.5])

with c_heat:
    st.markdown("#### Matriz de Demanda")
    orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    df_heat = df_f.groupby('Dia_Semana')['Ventas'].mean().reindex(orden_dias).reset_index()
    fig_heat = px.density_heatmap(df_f, x='Dia_Semana', y='Producto', z='Ventas', histfunc='avg', 
                                  color_continuous_scale='tealgrn', category_orders={'Dia_Semana': orden_dias})
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=11),
                            coloraxis_colorbar=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')))
    st.plotly_chart(fig_heat, use_container_width=True)

with c_anom:
    st.markdown("#### Detección Estadística de Anomalías")
    df_g = df_f.groupby('Fecha')['Ventas'].sum().reset_index()
    media, desviacion = df_g['Ventas'].mean(), df_g['Ventas'].std()
    df_g['Anomalia'] = np.where(abs(df_g['Ventas'] - media) > (2 * desviacion), True, False)
    
    fig_anom = go.Figure()
    fig_anom.add_trace(go.Scatter(x=df_g['Fecha'], y=df_g['Ventas'], mode='lines', name='Flujo Normal', line=dict(color='#00d2ff', width=2)))
    anomalias = df_g[df_g['Anomalia'] == True]
    fig_anom.add_trace(go.Scatter(x=anomalias['Fecha'], y=anomalias['Ventas'], mode='markers', name='Shock de Mercado', marker=dict(color='#ff4b4b', size=10, symbol='circle-open')))
    fig_anom.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=11), hovermode="x unified")
    st.plotly_chart(fig_anom, use_container_width=True)


# --- 9. BLOQUE 4: TERMINAL LOGÍSTICA (Limpia) ---
st.divider()
with st.expander("### 📋 Terminal de Acción Logística", expanded=True):
    resumen = df_f.groupby(['Ubicación', 'Producto']).agg(Ventas_Totales=('Ventas', 'sum'), Promedio_Diario=('Ventas', 'mean')).reset_index()
    resumen['Promedio_Diario'] = resumen['Promedio_Diario'].round(2)
    resumen['Estatus'] = np.where(resumen['Promedio_Diario'] < 30, '🔴 Riesgo Desabasto', '🟢 Óptimo')
    resumen['Acción Sugerida'] = np.where(resumen['Estatus'] == '🔴 Riesgo Desabasto', 'Aumentar Frecuencia', 'Mantener Surtido')

    c_tabla, c_export = st.columns([3, 1])
    with c_tabla:
        # Usamos pandas styler para colorear el semáforo
        st.dataframe(resumen.style.map(lambda x: 'color: #ff4b4b' if '🔴' in str(x) else ('color: #00e676' if '🟢' in str(x) else ''), subset=['Estatus']), use_container_width=True)

    with c_export:
        st.markdown("#### Exportar Base de Datos")
        csv = resumen.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Descargar Reporte CSV", data=csv, file_name='pepsico_reporte_metropolitano.csv', mime='text/csv')
        st.info("Formato listo para integración con SAP/Excel.")
