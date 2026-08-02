# Análisis Econométrico del Impacto de Shocks Macroeconómicos Externos en Ecuador (2010 - 2025)

**Autor:** Camilo Sebastian Pacheco Hurtado  
**Curso:** Econometría Avanzada / Series de Tiempo  
**Fecha:** Agosto 2026  

---

## Resumen Executive

El presente estudio evalúa el impacto dinámico de las perturbaciones externas (precio del petróleo y riesgo país EMBI) sobre el Producto Interno Bruto (PIB) real y el crédito del sistema financiero en la economía dolarizada de Ecuador. Utilizando datos trimestrales del Banco Central del Ecuador (BCE) para el periodo 2010Q1 - 2025Q4, se aplicaron pruebas de raíz unitaria (ADF) y el test de cointegración de Johansen. Los resultados confirmaron la existencia de $r=2$ relaciones de cointegración de largo plazo, justificando la estimación de un Modelo de Vector de Corrección de Errores (**VECM**).

---

## 1. Introducción y Marco Teórico

La economía ecuatoriana se caracteriza por su vulnerabilidad frente a shocks externos debido a la ausencia de una política monetaria autónoma bajo el régimen de dolarización. Las variaciones en los precios del crudo y las oscilaciones en la prima de riesgo país representan las principales fuentes de volatilidad macroeconómica.

---

## 2. Metodología y Agentes de Datos

El pipeline del proyecto fue estructurado bajo arquitectura modular de agentes de Inteligencia Artificial:

* **DataAgent (`agents/data_agent.py`):** Ingesta, transformación logarítmica ($\ln$) y cálculo de primeras diferencias ($\Delta \ln$).
* **EconometricsAgent (`agents/econometrics_agent.py`):** Pruebas de estacionariedad Augmented Dickey-Fuller (ADF) y test de Cointegración de Johansen.
* **Modelo Estimado:** VECM con 2 rezagos optimizados mediante criterio AIC.

---

## 3. Resultados Econométricos

### 3.1 Estacionariedad
Todas las variables en niveles fueron no estacionarias en niveles $I(1)$, pero alcanzaron estacionariedad al ser transformadas en primeras diferencias $I(0)$ con niveles de significancia del 5%.

### 3.2 Cointegración y Dinámica de Corto/Largo Plazo
La prueba de Johansen mostró $r=2$ vectores de cointegración. Las Funciones Impulso-Respuesta (IRF) indican que:
1. Un shock positivo de 1 desviación estándar en el precio del petróleo incrementa de forma persistente el PIB real a partir del segundo trimestre.
2. Un incremento en el riesgo país (EMBI) genera una contracción inmediata sobre la oferta de crédito y reduce la actividad económica.

---

## 4. Conclusiones y Recomendaciones de Política

* La regla de sostenibilidad fiscal en Ecuador debe mantener fondos de estabilización petrolera para mitigar los ciclos recesivos causados por la volatilidad externa.
* El canal del crédito actúa como el principal mecanismo de transmisión entre los shocks de riesgo financiero externo y la actividad productiva local.
