# agents/data_agent.py
import pandas as pd
import numpy as np
from pathlib import Path

class DataAgent:
    """
    Agente para la ingesta, limpieza, transformación logarítmica y
    diferenciación de series macroeconómicas del Ecuador.
    """
    def __init__(self, raw_data_path: str):
        self.raw_path = Path(raw_data_path)
        self.df = None
        self.df_processed = None

    def load_data(self) -> pd.DataFrame:
        """Carga los datos en bruto desde CSV."""
        if not self.raw_path.exists():
            raise FileNotFoundError(f"No se encontró el archivo en: {self.raw_path}")
        
        self.df = pd.read_csv(self.raw_path, index_col=0, parse_dates=True)
        print(f"🤖 [DataAgent]: Datos cargados correctamente. {self.df.shape[0]} observaciones, {self.df.shape[1]} variables.")
        return self.df

    def transform_variables(self, vars_to_transform: list) -> pd.DataFrame:
        """
        Aplica transformación logarítmica a las variables seleccionadas
        y calcula las primeras diferencias para análisis econométrico.
        """
        if self.df is None:
            self.load_data()

        self.df_processed = pd.DataFrame(index=self.df.index)

        for col in vars_to_transform:
            if col in self.df.columns:
                # 1. Conservar variable en nivel original
                self.df_processed[col] = self.df[col]
                # 2. Transformación Logarítmica
                self.df_processed[f'L_{col}'] = np.log(self.df[col])
                # 3. Primera Diferencia del Logaritmo (Tasa de variación / Crecimiento)
                self.df_processed[f'D_L_{col}'] = self.df_processed[f'L_{col}'].diff()
            else:
                print(f"⚠️ Advertencia: La variable '{col}' no se encuentra en el Dataset.")

        # Eliminar la primera fila que contendrá NaN por la diferencia
        self.df_processed = self.df_processed.dropna()
        print("🤖 [DataAgent]: Transformaciones logarítmicas y diferencias completadas exitosamente.")
        return self.df_processed

    def save_processed_data(self, output_path: str):
        """Guarda la base procesada en data/processed/."""
        if self.df_processed is None:
            raise ValueError("No hay datos procesados para guardar. Ejecuta transform_variables() primero.")
            
        out_p = Path(output_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        self.df_processed.to_csv(out_p)
        print(f"💾 [DataAgent]: Base procesada guardada exitosamente en: {output_path}")

if __name__ == "__main__":
    # Ingesta y procesamiento
    agent = DataAgent("data/raw/datos_bce_trimestral.csv")
    agent.load_data()
    agent.transform_variables(vars_to_transform=['PIB', 'PET', 'EMBI', 'CRED'])
    agent.save_processed_data("data/processed/datos_procesados.csv")