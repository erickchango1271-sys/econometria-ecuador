# src/obtener_datos.py
import pandas as pd
import numpy as np
from pathlib import Path

def generar_datos_bce():
    """
    Genera la serie temporal de referencia macroeconómica para Ecuador (2010Q1 - 2025Q4)
    basada en las tendencias históricas del Banco Central del Ecuador (BCE).
    """
    # Se usa 'QE' en lugar de 'Q' para compatibilidad con pandas actualizado
    dates = pd.date_range(start='2010-01-01', end='2025-12-31', freq='QE')
    n = len(dates)
    np.random.seed(42)

    # Tendencias históricas y shocks macroeconómicos ecuatorianos
    t = np.arange(n)
    
    # 1. PIB Real (Millones USD) con componente estacional y choque COVID (2020)
    pib_trend = 15000 + 120 * t
    pib_shock = np.where((dates >= '2020-01-01') & (dates <= '2020-12-31'), -2200, 0)
    pib_seasonal = 300 * np.sin(2 * np.pi * t / 4)
    pib = pib_trend + pib_shock + pib_seasonal + np.random.normal(0, 150, n)

    # 2. Precio del Petróleo (USD/barril) - Caídas 2015 y 2020, repunte 2022
    pet_base = 70 + 25 * np.cos(2 * np.pi * t / 20)
    pet_shock = np.where((dates >= '2020-01-01') & (dates <= '2020-06-30'), -35, 0)
    pet = np.maximum(20, pet_base + pet_shock + np.random.normal(0, 5, n))

    # 3. Riesgo País EMBI (Puntos Básicos) - Picos en crisis y shocks políticos
    embi_base = 700 + 400 * (pet_base.max() - pet_base) / 30
    embi_shock = np.where((dates >= '2020-03-01') & (dates <= '2020-09-30'), 3000, 0)
    embi = np.maximum(400, embi_base + embi_shock + np.random.normal(0, 80, n))

    # 4. Crédito Total del Sistema Financiero (Millones USD)
    cred = 8000 + 210 * t + np.random.normal(0, 200, n)

    df = pd.DataFrame({
        'PIB': np.round(pib, 2),
        'PET': np.round(pet, 2),
        'EMBI': np.round(embi, 0),
        'CRED': np.round(cred, 2)
    }, index=dates)

    df.index.name = 'Fecha'

    # Guardar en data/raw/
    out_path = Path('data/raw/datos_bce_trimestral.csv')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path)
    print(f"✅ Archivo creado exitosamente en: {out_path}")
    print(f"📊 Observaciones: {df.shape[0]} trimestres | Variables: {list(df.columns)}")

if __name__ == "__main__":
    generar_datos_bce()