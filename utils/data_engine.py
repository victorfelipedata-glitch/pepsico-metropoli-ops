import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_hyper_data():
    np.random.seed(42)
    dias = pd.date_range(start="2026-01-01", periods=60)
    
    locales = {
        'Cuauhtémoc': [19.4326, -99.1332], 'Miguel Hidalgo': [19.4323, -99.1947],
        'Azcapotzalco': [19.4853, -99.1821], 'GAM': [19.4840, -99.1150],
        'Venustiano Carranza': [19.4305, -99.1000], 'Iztacalco': [19.3950, -99.0980],
        'Benito Juárez': [19.3798, -99.1585], 'Coyoacán': [19.3490, -99.1620],
        'Iztapalapa': [19.3553, -99.0622], 'Álvaro Obregón': [19.3590, -99.2310],
        'Tlalpan': [19.2890, -99.1650], 'Xochimilco': [19.2620, -99.1030],
        'Naucalpan': [19.4785, -99.2331], 'Tlalnepantla': [19.5437, -99.1947],
        'Atizapán': [19.5546, -99.2483], 'Ecatepec': [19.6018, -99.0449],
        'Nezahualcóyotl': [19.4042, -99.0146], 'Cuautitlán Izcalli': [19.6433, -99.2158],
        'Huixquilucan': [19.3585, -99.3541], 'Chalco': [19.2611, -98.8978],
        'Tultitlán': [19.6480, -99.1740], 'Coacalco': [19.6330, -99.0960],
        'Chimalhuacán': [19.4210, -98.9550], 'Texcoco': [19.5110, -98.8820],
        'La Paz': [19.3560, -98.9800]
    }
    
    productos = [
        'Sabritas Original', 'Sabritas Adobadas', 'Ruffles Queso', 'Doritos Nacho', 
        'Doritos Incógnita', 'Cheetos Torciditos', 'Cheetos Flamin Hot', 'Tostitos Salsa Verde', 
        'Fritos Sal', 'Churrumais', 'Pepsi 600ml', 'Pepsi Black', '7UP', 'Mirinda', 
        'Gatorade Naranja', 'Gatorade Moras', 'Epura 600ml', 'Emperador Chocolate', 
        'Chokis', 'Marias Gamesa', 'Mamut', 'Quaker Avena', 'Rockaleta'
    ]
    
    data = []
    for loc, coords in locales.items():
        for prod in productos:
            base = np.random.poisson(lam=np.random.randint(20, 100), size=60)
            if np.random.rand() > 0.85:
                dia_random = np.random.randint(10, 50)
                base[dia_random] = base[dia_random] * np.random.choice([0.1, 3.0])
                
            for d, v in zip(dias, base):
                data.append([d, loc, prod, int(v), coords[0], coords[1]])
                
    df_temp = pd.DataFrame(data, columns=['Fecha', 'Ubicación', 'Producto', 'Ventas', 'lat', 'lon'])
    dias_esp = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miércoles', 'Thursday':'Jueves', 'Friday':'Viernes', 'Saturday':'Sábado', 'Sunday':'Domingo'}
    df_temp['Dia_Semana'] = df_temp['Fecha'].dt.day_name().map(dias_esp)
    return df_temp
