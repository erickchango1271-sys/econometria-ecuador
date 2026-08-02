# agents/econometrics_agent.py
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.vecm import coint_johansen

class TimeSeriesAgent:
    """
    Agente econométrico para automatizar pruebas de estacionariedad,
    cointegración y selección de rezagos en modelos VAR/VECM.
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data.dropna()

    def adf_test(self, column: str) -> dict:
        """Realiza la prueba Augmented Dickey-Fuller para una serie."""
        res = adfuller(self.data[column], autolag='AIC')
        return {
            'Variable': column,
            'ADF Statistic': res[0],
            'p-value': res[1],
            'Lags Used': res[2],
            'Stationary (5%)': res[1] < 0.05
        }

    def select_lag_order(self, maxlags: int = 8):
        """Determina el número óptimo de rezagos basado en criterios de información."""
        model = VAR(self.data)
        results = model.select_order(maxlags=maxlags)
        return results

    def johansen_coint_test(self, det_order: int = 0, k_ar_diff: int = 1):
        """Ejecuta la prueba de cointegración de Johansen."""
        res = coint_johansen(self.data, det_order, k_ar_diff)
        return {
            'trace_stat': res.lr1,
            'trace_crit_vals': res.cvt,
            'eigen_stat': res.lr2,
            'eigen_crit_vals': res.cvm
        }