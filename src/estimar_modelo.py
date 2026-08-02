# src/estimar_modelo.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.api import VAR

def estimar_e_interpretar():
    data_path = Path("data/processed/datos_procesados.csv")
    if not data_path.exists():
        print("⚠️ No se encontró la base procesada. Ejecuta agents/data_agent.py primero.")
        return

    df = pd.read_csv(data_path, index_col=0, parse_dates=True)
    vars_diff = ['D_L_PIB', 'D_L_PET', 'D_L_EMBI', 'D_L_CRED']
    data_model = df[vars_diff].dropna()

    print("📊 Estimando modelo VAR para análisis de Impulso-Respuesta y FEVD...")
    model = VAR(data_model)
    results = model.fit(2)

    # 1. Graficar Funciones Impulso-Respuesta (IRF)
    plt.style.use('seaborn-v0_8-whitegrid')
    irf = results.irf(periods=10)
    
    fig = irf.plot(orth=True, figsize=(12, 10))
    fig.suptitle('Funciones Impulso-Respuesta (IRF) Ortogonalizadas - 10 Trimestres', fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    out_irf = Path("outputs/figures/03_irf_impulso_respuesta.png")
    out_irf.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_irf, dpi=300)
    plt.close()
    print(f"✅ Gráfico de IRF guardado exitosamente en: {out_irf}")

    # 2. Descomposición de Varianza del Error de Pronóstico (FEVD)
    fevd = results.fevd(periods=10)
    fig_fevd = fevd.plot(figsize=(12, 10))
    fig_fevd.suptitle('Descomposición de la Varianza del Error de Pronóstico (FEVD)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    out_fevd = Path("outputs/figures/04_fevd_varianza.png")
    plt.savefig(out_fevd, dpi=300)
    plt.close()
    print(f"✅ Gráfico de FEVD guardado exitosamente en: {out_fevd}")

if __name__ == "__main__":
    estimar_e_interpretar()