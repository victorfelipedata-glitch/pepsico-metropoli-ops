import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode

# --- IMPORTAMOS NUESTROS PROPIOS MÓDULOS ---
from utils.styles import apply_cyber_theme, custom_metric_card
from utils.data_engine import load_hyper_data

# --- 1. SETUP CORPORATIVO ---
st.set_page_config(page_title="PepsiCo | Centro de Comando", layout="wide", initial_sidebar_state="expanded")

# --- 2. APLICAR ESTILOS Y CARGAR DATOS ---
apply_cyber_theme()
df = load_hyper_data()

# --- 3. BARRA LATERAL (Filtros + SIMULADOR + TOOLTIPS) ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Pepsi_logo_2014.svg/512px-Pepsi_logo_2014.svg.png", width=120)

st.sidebar.markdown("# 🔱 Filtros de Red")
st.sidebar.write("Configura la vista de operaciones.")
st.sidebar.divider()

with st.sidebar.expander("📍 Nodos Metropolitanos", expanded=True):
    default_zonas = ['Naucalpan', 'Ecatepec', 'Iztapalapa', 'GAM', 'Cuauhtémoc', 'Atizapán', 'Tlalnepantla']
    zona_sel = st.multiselect("Seleccionar Nodos:", options=list(df['Ubicación'].unique()), default=default_zonas, help="Selecciona las zonas geográficas que deseas monitorear.", label_visibility="collapsed")

with st.sidebar.expander("🥤 Carga Comercial (SKUs)", expanded=True):
    prod_sel = st.multiselect("Seleccionar SKUs:", options=list(df['Producto'].unique()), default=['Sabritas Original', 'Pepsi Black', 'Doritos Incógnita'], help="Selecciona los productos específicos para analizar su desplazamiento.", label_visibility="collapsed")

with st.sidebar.expander("⏱️ Ventana de Análisis", expanded=True):
    min_date = df['Fecha'].min().date()
    max_date = df['Fecha'].max().date()
    date_range = st.date_input("Rango temporal:", value=(min_date, max_date), min_value=min_date, max_value=max_date, help="Define el periodo de tiempo para el cálculo de métricas e histórico.", label_visibility="collapsed")

# --- SIMULADOR DE ESCENARIOS ---
st.sidebar.divider()
st.sidebar.markdown("### 🧪 Simulador de Escenarios")
st.sidebar.write("Ajusta la demanda proyectada para prever shocks.")
factor_sim = st.sidebar.slider("Incremento de Demanda (%)", -50, 100, 0, help="Simula un evento (ej. Buen Fin o partido de fútbol) aumentando o disminuyendo las ventas base.")

# Lógica de fechas
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
].copy()

# APLICAR MATEMÁTICAS DEL SIMULADOR
df_f['Ventas'] = (df_f['Ventas'] * (1 + factor_sim / 100)).astype(int)

if df_f.empty:
    st.warning("⚠️ No hay datos para los filtros seleccionados. Amplía el rango o selecciona otros nodos.")
    st.stop()


# --- 4. ENCABEZADO CENTRAL ESTILO SAMSUNG (HERO BANNER) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;800&display=swap');

.hero-container {
    position: relative;
    /* Usamos una imagen abstracta oscura de alta calidad de fondo */
    background-image: url('https://images.unsplash.com/photo-1614064641936-3899d907016ea?q=80&w=2000&auto=format&fit=crop'); 
    background-size: cover;
    background-position: center;
    border-radius: 20px;
    padding: 60px 40px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    overflow: hidden;
    font-family: 'Inter', sans-serif;
}

.hero-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    /* Un gradiente que va de negro sólido a transparente para que el texto se lea perfecto */
    background: linear-gradient(90deg, rgba(11, 14, 20, 0.95) 0%, rgba(11, 14, 20, 0.6) 50%, rgba(11, 14, 20, 0.1) 100%);
    z-index: 1;
}

.hero-content {
    position: relative;
    z-index: 2;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #0284c7, #38bdf8); /* El azul premium */
    color: white;
    padding: 6px 16px;
    border-radius: 30px;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 20px;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 10px;
    line-height: 1.1;
    letter-spacing: -1.5px;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    font-weight: 300;
    max-width: 600px;
    line-height: 1.5;
}
</style>

<div class="hero-container">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <div class="hero-badge">✨ Inteligencia Artificial</div>
        <div class="hero-title">Centro de<br>Comando PepsiCo</div>
        <div class="hero-subtitle">Monitorización de Inventario y Demanda en el Valle de México. Resolviendo logística compleja a través de modelos predictivos y visualización geoespacial en tiempo real.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Borramos la alerta de info anterior y dejamos que el banner haga el trabajo visual
st.divider()

# --- INSIGHTS TRADUCIDOS ---
st.info("💡 **Análisis del Sistema:** " + 
    (f"⚠️ Se simula un shock de demanda del {factor_sim}%. " if factor_sim != 0 else "") +
    f"El SKU con mayor rotación en este periodo es **{df_f.groupby('Producto')['Ventas'].sum().idxmax()}**. " +
    f"Se recomienda asegurar la logística en la zona de **{df_f.groupby('Ubicación')['Ventas'].sum().idxmax()}** debido a su alto volumen proyectado.")

st.divider()

# DEFINIMOS LA NUEVA PALETA CORPORATIVA (Menos neón, más profesional)
paleta_unificada = ['#0f172a', '#1e293b', '#0284c7', '#38bdf8']
color_acento = '#38bdf8' # Azul acero/cielo

# --- 5. ESTRUCTURA DE PESTAÑAS (TABS) ---
tab_monitor, tab_predict, tab_logistics = st.tabs(["🌐 Monitor Global", "🧠 Inteligencia Predictiva", "📋 Gestión Logística"])

# ==========================================
# PESTAÑA 1: MONITOR GLOBAL
# ==========================================
with tab_monitor:
    st.markdown("### 📊 Indicadores Clave de Red")
    k1, k2, k3, k4 = st.columns(4)

    vol_sum = df_f['Ventas'].sum()
    with k1:
        custom_metric_card("Volumen Total", f"{int(vol_sum):,} u", delta=f"{len(df_f)} registros procesados", is_accent=False, help_text="Suma total de unidades desplazadas.")

    nodos_sat = len(zona_sel)
    with k2:
        custom_metric_card("Nodos Activos", f"{nodos_sat} / 25", delta="📡 Red Central Estable", delta_positive=True, is_accent=False, help_text="Cantidad de centros de distribución activos.")

    pico_max = int(df_f['Ventas'].max())
    with k3:
        custom_metric_card("Pico de Demanda", f"{pico_max} u", delta="⚠️ Alerta Nivel 1" if pico_max > 150 else "⚡ Normal", delta_positive=pico_max <= 150, is_accent=True, help_text="El valor de venta individual más alto detectado.")

    inventario_est = vol_sum * 22.5
    with k4:
        custom_metric_card("Inventario Est.", f"${int(inventario_est):,.0f}", delta="Pesos Mexicanos (MXN)", is_accent=False, help_text="Valorización aproximada del inventario.")

    st.divider()
    st.markdown("### 📍 Módulo Geoespacial y Multivariable")
    c_map, c_radar = st.columns([2, 1])

    with c_map:
        st.write("Visualización espacial de nodos y volumen de ventas.")
        fig_map = px.scatter_mapbox(df_f.groupby('Ubicación', as_index=False).agg({'Ventas':'sum', 'lat':'first', 'lon':'first'}), 
                                    lat='lat', lon='lon', size='Ventas', color='Ventas', color_continuous_scale=paleta_unificada,
                                    hover_name='Ubicación', zoom=9.2, mapbox_style="carto-darkmatter")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', coloraxis_colorbar=dict(title=dict(text='Ventas', font=dict(color='white')), tickfont=dict(color='white')))
        st.plotly_chart(fig_map, use_container_width=True)

    with c_radar:
        st.write("Análisis Multivariable de Eficiencia.")
        categorias = ['Demanda Base', 'Penetración', 'Estabilidad', 'Margen Ops', 'Rotación']
        valores = [np.random.randint(70, 100) for _ in range(5)]
        fig_radar = go.Figure(data=go.Scatterpolar(r=valores, theta=categorias, fill='toself', fillcolor='rgba(56, 189, 248, 0.15)', line=dict(color=color_acento, width=2)))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='gray'), bgcolor='rgba(0,0,0,0)'), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11))
        st.plotly_chart(fig_radar, use_container_width=True)

    st.divider()
    st.markdown("### 🟦 Topografía de Mercado (Dominancia)", help="Jerarquía de ventas por zona (cuadros grandes) y producto (cuadros internos).")
    fig_tree = px.treemap(df_f, path=[px.Constant("Valle de México"), 'Ubicación', 'Producto'], values='Ventas', color='Ventas', color_continuous_scale=paleta_unificada)
    fig_tree.update_layout(margin=dict(t=10, l=10, r=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=13))
    fig_tree.update_traces(marker=dict(line=dict(color='#0d1117', width=3)), root_color="#0d1117")
    st.plotly_chart(fig_tree, use_container_width=True)

# ==========================================
# PESTAÑA 2: INTELIGENCIA PREDICTIVA
# ==========================================
with tab_predict:
    st.markdown("### ⏱️ Análisis de Series Temporales y Detección de Shocks")
    c_heat, c_anom = st.columns([1, 1.5])

    with c_heat:
        st.markdown("#### Matriz de Demanda")
        orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        df_heat = df_f.groupby('Dia_Semana')['Ventas'].mean().reindex(orden_dias).reset_index()
        fig_heat = px.density_heatmap(df_f, x='Dia_Semana', y='Producto', z='Ventas', histfunc='avg', color_continuous_scale=paleta_unificada, category_orders={'Dia_Semana': orden_dias})
        fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11), coloraxis_colorbar=dict(title=dict(font=dict(color='white')), tickfont=dict(color='white')))
        st.plotly_chart(fig_heat, use_container_width=True)

    with c_anom:
        st.markdown("#### Detección Estadística de Anomalías")
        df_g = df_f.groupby('Fecha')['Ventas'].sum().reset_index()
        media, desviacion = df_g['Ventas'].mean(), df_g['Ventas'].std()
        df_g['Anomalia'] = np.where(abs(df_g['Ventas'] - media) > (2 * desviacion), True, False)
        
        fig_anom = go.Figure()
        fig_anom.add_trace(go.Scatter(x=df_g['Fecha'], y=df_g['Ventas'], mode='lines', name='Flujo Normal', line=dict(color=color_acento, width=2)))
        anomalias = df_g[df_g['Anomalia'] == True]
        fig_anom.add_trace(go.Scatter(x=anomalias['Fecha'], y=anomalias['Ventas'], mode='markers', name='Shock de Mercado', marker=dict(color='#f87171', size=10, symbol='circle-open'))) # Rojo para alertas
        fig_anom.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11), hovermode="x unified")
        st.plotly_chart(fig_anom, use_container_width=True)

    st.divider()
    st.markdown("### 🧠 Proyección Predictiva (Machine Learning)", help="Modelo de Regresión Lineal entrenado en tiempo real para pronosticar la demanda a 7 días.")

    df_ml = df_f.groupby('Fecha')['Ventas'].sum().reset_index()
    df_ml['Dias_Numericos'] = (df_ml['Fecha'] - df_ml['Fecha'].min()).dt.days

    if len(df_ml) > 3:
        X = df_ml[['Dias_Numericos']]
        y = df_ml['Ventas']
        
        modelo = LinearRegression()
        modelo.fit(X, y)
        
        ultimo_dia = df_ml['Dias_Numericos'].max()
        dias_futuros_num = pd.DataFrame({'Dias_Numericos': range(ultimo_dia + 1, ultimo_dia + 8)})
        fechas_futuras = pd.date_range(start=df_ml['Fecha'].max() + pd.Timedelta(days=1), periods=7)
        
        predicciones = modelo.predict(dias_futuros_num)
        tendencia = "al alza 📈" if modelo.coef_[0] > 0 else "a la baja 📉"
        
        c_pred, c_texto = st.columns([2, 1])
        
        with c_pred:
            fig_ml = go.Figure()
            fig_ml.add_trace(go.Scatter(x=df_ml['Fecha'], y=df_ml['Ventas'], mode='lines', name='Histórico Real', line=dict(color='#94a3b8', width=2)))
            fig_ml.add_trace(go.Scatter(x=df_ml['Fecha'], y=modelo.predict(X), mode='lines', name='Ajuste ML', line=dict(color='#0284c7', width=2, dash='dot')))
            fig_ml.add_trace(go.Scatter(x=fechas_futuras, y=predicciones, mode='lines+markers', name='Pronóstico 7 Días', line=dict(color=color_acento, width=3), marker=dict(size=6)))
            
            fig_ml.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11), hovermode="x unified", margin=dict(t=10, b=10, l=10, r=10))
            st.plotly_chart(fig_ml, use_container_width=True)
            
        with c_texto:
            st.markdown("#### Resultado del Modelo")
            st.write("El algoritmo analiza la dispersión histórica y calcula la línea de mejor ajuste para proyectar requerimientos logísticos.")
            st.info(f"**Insight Predictivo:**\nLa tendencia matemática para esta red va **{tendencia}**.\n\nPara el día {fechas_futuras[-1].strftime('%d de %b')}, el modelo estima una demanda de **{int(predicciones[-1])} unidades**.")
    else:
        st.warning("⚠️ No hay suficientes datos en este rango para entrenar el modelo predictivo. Amplía la ventana de análisis.")


# ==========================================
# PESTAÑA 3: GESTIÓN LOGÍSTICA (CON AG-GRID ENTERPRISE)
# ==========================================
with tab_logistics:
    st.markdown("### 📋 Terminal de Acción Logística Avanzada")
    st.write("Sistema de gestión interactivo. Usa el menú lateral de la tabla para agrupar, filtrar y exportar como en Excel.")
    
    resumen = df_f.groupby(['Ubicación', 'Producto']).agg(Ventas_Totales=('Ventas', 'sum'), Promedio_Diario=('Ventas', 'mean')).reset_index()
    resumen['Promedio_Diario'] = resumen['Promedio_Diario'].round(2)
    resumen['Estatus'] = np.where(resumen['Promedio_Diario'] < 30, '🔴 Riesgo', '🟢 Óptimo')
    resumen['Acción'] = np.where(resumen['Estatus'] == '🔴 Riesgo', 'Aumentar', 'Mantener')

    # --- CONFIGURACIÓN MAGIA AG-GRID ---
    gb = GridOptionsBuilder.from_dataframe(resumen)
    gb.configure_pagination(paginationAutoPageSize=True) # Paginación automática
    gb.configure_side_bar() # Activa el panel lateral de filtros avanzados tipo Excel
    gb.configure_selection('multiple', use_checkbox=True) # Permite seleccionar filas con checkboxes
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    gridOptions = gb.build()

    # --- RENDERIZADO DE LA TABLA ---
    AgGrid(
        resumen,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        theme='streamlit', # Se adapta automáticamente a tu fondo oscuro
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        update_mode='MODEL_CHANGED'
    )
    
    st.divider()
    c_empty, c_export = st.columns([3, 1])
    with c_export:
        csv = resumen.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Exportar Matriz a SAP", data=csv, file_name='logistica_pepsico_matriz.csv', mime='text/csv')


# --- FOOTER CLASIFICADO ---
st.divider()
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.9rem; margin-top: 20px;">
    © 2026 PepsiCo Intelligence System <br>
    Modelo de monitorización desarrollado por <b style="color: #38bdf8;">Data Analyst Víctor Antonio</b>
</div>
""", unsafe_allow_html=True)
