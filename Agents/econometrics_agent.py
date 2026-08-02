# agents/econometrics_agent.py
import pandas as pd
import numpy as np
import json
from pathlib import Path
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen, VECM

class EconometricsAgent:
    """
    Agente para pruebas de raíz unitaria (ADF), selección de rezagos,
    cointegración de Johansen y estimación de VAR/VECM.
    """
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.df = pd.read_csv(self.data_path, index_col=0, parse_dates=True)
        self.vars_levels = ['L_PIB', 'L_PET', 'L_EMBI', 'L_CRED']
        self.vars_diff = ['D_L_PIB', 'D_L_PET', 'D_L_EMBI', 'D_L_CRED']

    def test_stationarity_adf(self) -> pd.DataFrame:
        """Ejecuta la prueba Augmented Dickey-Fuller en niveles y en diferencias."""
        results = []
        for col in self.vars_levels:
            # En Niveles
            res_level = adfuller(self.df[col].dropna(), autolag='AIC')
            # En Diferencias
            diff_col = f'D_{col}'
            res_diff = adfuller(self.df[diff_col].dropna(), autolag='AIC')

            results.append({
                'Variable': col,
                'ADF_Nivel': round(res_level[0], 4),
                'p_val_Nivel': round(res_level[1], 4),
                'Estacionaria_Nivel': res_level[1] < 0.05,
                'ADF_Diff': round(res_diff[0], 4),
                'p_val_Diff': round(res_diff[1], 4),
                'Estacionaria_Diff': res_diff[1] < 0.05
            })
        
        adf_df = pd.DataFrame(results)
        print("🤖 [EconometricsAgent]: Pruebas ADF completadas.")
        return adf_df

    def select_lag_order(self, maxlags=6):
        """Selecciona el número óptimo de rezagos para el VAR."""
        data_var = self.df[self.vars_levels].dropna()
        model = VAR(data_var)
        select_res = model.select_order(maxlags=maxlags)
        print(f"🤖 [EconometricsAgent]: Selección de rezagos (AIC recomienda: {select_res.aic}).")
        return select_res

    def johansen_cointegration(self, k_ar_diff=1):
        """Ejecuta la prueba de Cointegración de Johansen."""
        data_coint = self.df[self.vars_levels].dropna()
        # det_order = 0 (constante dentro de la ecuación de cointegración)
        joh_res = coint_johansen(data_coint, det_order=0, k_ar_diff=k_ar_diff)
        
        trace_stat = joh_res.lr1
        crit_vals_95 = joh_res.cvt[:, 1] # 5% valor crítico
        
        r_count = sum(trace_stat > crit_vals_95)
        print(f"🤖 [EconometricsAgent]: Johansen completado. Relaciones de cointegración (r) detectadas al 5%: {r_count}")
        return r_count, trace_stat, crit_vals_95

    def fit_var_or_vecm(self, lags=2):
        """
        Determina automáticamente si estimar un VECM (si hay cointegración)
        o un VAR en diferencias (si no la hay).
        """
        r_count, _, _ = self.johansen_cointegration(k_ar_diff=lags-1)
        
        results_summary = {}
        out_dir = Path("outputs/results")
        out_dir.mkdir(parents=True, exist_ok=True)

        if r_count > 0:
            print(f"📊 Se detectó Cointegración (r={r_count}). Estimando Modelo VECM...")
            vecm_model = VECM(self.df[self.vars_levels].dropna(), k_ar_diff=lags-1, coint_rank=r_count)
            vecm_fit = vecm_model.fit()
            
            results_summary['model_type'] = 'VECM'
            results_summary['coint_rank'] = int(r_count)  # Convertido a int nativo
            results_summary['lags'] = int(lags)            # Convertido a int nativo
            print("✅ Modelo VECM estimado exitosamente.")
        else:
            print("📊 No se detectó Cointegración. Estimando Modelo VAR en primeras diferencias...")
            var_model = VAR(self.df[self.vars_diff].dropna())
            var_fit = var_model.fit(lags)
            
            results_summary['model_type'] = 'VAR_Diferencias'
            results_summary['lags'] = int(lags)
            print("✅ Modelo VAR estimado exitosamente.")

        # Exportar resumen a JSON para consumo del Dashboard en Vercel
        with open(out_dir / "modelo_resumen.json", "w") as f:
            json.dump(results_summary, f, indent=4)

        return results_summary