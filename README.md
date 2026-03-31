# 🌐 PepsiCo Intelligence System | Command Center Titanium

![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Data_Viz-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

Plataforma analítica de operaciones diseñada para la monitorización de inventarios, detección de anomalías y predicción de demanda en el Valle de México.

## 🚀 Funcionalidades Principales

* **Módulo Geoespacial Multivariable:** Mapeo de densidad de ventas por nodo metropolitano (Plotly Mapbox).
* **Escáner de Anomalías Estadísticas:** Algoritmo de detección de shocks de mercado basado en desviaciones estándar sobre el flujo normal.
* **Simulador de Escenarios Estocásticos:** Motor interactivo para evaluar el impacto de eventos atípicos (ej. Buen Fin, contingencias) alterando la matriz de demanda.
* **Proyección Predictiva (Machine Learning):** Modelo de regresión lineal entrenado en tiempo real que evalúa la dispersión histórica para pronosticar requerimientos logísticos a 7 días.

## 🛠️ Arquitectura del Software
El proyecto está construido bajo un enfoque modular para garantizar la escalabilidad:
* `app.py`: Frontend interactivo y orquestación de componentes.
* `utils/data_engine.py`: Motor de simulación de datos masivos.
* `utils/styles.py`: Inyección de CSS puro (Glassmorphism & Cyber-theme) y componentes UI personalizados.

## 🧠 Lógica Analítica
Como parte de la estrategia de Inteligencia de Negocios, el sistema no solo visualiza datos, sino que los interpreta. Utiliza modelos matemáticos para generar **Insights Narrativos**, traduciendo cálculos complejos en recomendaciones logísticas en lenguaje natural.

---
*Desarrollado por **Víctor Antonio** - Data Analyst & Applied Mathematics*
