# dashboard/app.py
import streamlit as st
import pandas as pd
import json
from pathlib import Path

st.set_page_config(
    page_title="Dashboard Econométrico - Ecuador",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análisis Econométrico del Impacto de Shocks Externos en Ecuador")
st.markdown("---")

# Cargar resumen del modelo
results_path = Path("outputs/results/modelo_resumen.json")
if results_path.exists():
    with open(results_path, "r") as f:
        summary = json.load(f)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Modelo Estimado", summary.get("model_type", "N/A"))
    col2.metric("Rango de Cointegración (r)", summary.get("coint_rank", "N/A"))
    col3.metric("Rezagos (Lags)", summary.get("lags", "N/A"))

st.markdown("---")
st.subheader("📈 Resultados Visuales y Diagnósticos")

tab1, tab2, tab3 = st.tabs(["Niveles y Diferencias", "Funciones Impulso-Respuesta (IRF)", "Descomposición de Varianza (FEVD)"])

with tab1:
    st.image("outputs/figures/01_series_niveles.png", caption="Evolución en Niveles de las Variables", use_container_width=True)
    st.image("outputs/figures/02_series_diferencias.png", caption="Primeras Diferencias Logarítmicas", use_container_width=True)

with tab2:
    st.image("outputs/figures/03_irf_impulso_respuesta.png", caption="Respuestas Dinámicas ante Shocks Externos", use_container_width=True)

with tab3:
    st.image("outputs/figures/04_fevd_varianza.png", caption="Descomposición de la Varianza del Error de Pronóstico", use_container_width=True)