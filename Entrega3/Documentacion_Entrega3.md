# Documentación Entrega 3 - Proyecto de Machine Learning

## 1. Información del Proyecto
*   **Contexto:** Análisis de ventas minoristas para predecir comportamientos de compra y estimar ingresos.
*   **Datos:** Dataset sintético realista con 130 productos (Alimentos, Limpieza, Higiene), clientes con datos demográficos y transacciones de ventas generadas.

## 2. Objetivos
El proyecto tiene dos objetivos principales de Machine Learning:
1.  **Clasificación:** Predecir la **Categoría del Producto** que un cliente comprará basándose en su ubicación, medio de pago y el monto de la transacción. Esto ayuda a entender patrones de consumo.
2.  **Regresión:** Estimar el **Importe Total** de una venta basándose en la categoría, cantidad de productos y datos del cliente. Esto es útil para proyecciones de flujo de caja.

## 3. Algoritmo Elegido y Justificación
Se seleccionó **Random Forest** (Bosque Aleatorio) para ambas tareas:
*   **RandomForestClassifier** para la clasificación.
*   **RandomForestRegressor** para la regresión.

**Justificación:**
*   **Robustez:** Maneja bien tanto variables numéricas como categóricas y es menos propenso al sobreajuste (overfitting) que un árbol de decisión simple.
*   **Versatilidad:** Funciona excelentemente para clasificación multiclase y regresión.
*   **Interpretabilidad:** Permite extraer la "importancia de las variables" (Feature Importance), lo cual es crucial para el negocio.

## 4. Entradas (X) y Salida (y)

### Modelo 1: Clasificación
*   **Entradas (X):**
    *   `ciudad_n`: Ciudad del cliente (codificada numéricamente).
    *   `pago_n`: Medio de pago utilizado.
    *   `mes`: Mes de la transacción.
    *   `trimestre`: Trimestre del año.
    *   `cantidad`: Cantidad de unidades compradas.
    *   `importe`: Monto gastado.
*   **Salida (y):**
    *   `categoria_n`: Categoría del producto (Alimentos, Limpieza, Higiene personal).

### Modelo 2: Regresión
*   **Entradas (X):**
    *   `ciudad_n`: Ciudad del cliente.
    *   `pago_n`: Medio de pago.
    *   `mes`: Mes de la transacción.
    *   `categoria_n`: Categoría del producto.
    *   `cantidad`: Cantidad de unidades.
*   **Salida (y):**
    *   `importe`: Valor monetario total de la venta.

## 5. Métricas de Evaluación
*   **Para Clasificación:**
    *   **Accuracy (Precisión Global):** Porcentaje total de predicciones correctas.
    *   **Matriz de Confusión:** Para visualizar dónde se confunde el modelo entre clases.
    *   **Precision, Recall y F1-Score:** Métricas detalladas por cada clase.
*   **Para Regresión:**
    *   **R2 Score (Coeficiente de Determinación):** Indica qué tanta varianza de los datos es explicada por el modelo (1.0 es perfecto).
    *   **RMSE (Root Mean Squared Error):** El error promedio en la misma unidad que la variable objetivo (pesos/moneda).

## 6. Implementación y Entrenamiento
*   **División de Datos:** Se utilizó `train_test_split` con una proporción de **80% entrenamiento** y **20% prueba**.
*   **Entrenamiento:** El modelo se entrenó con 3000 registros de ventas generados sintéticamente para asegurar robustez estadística.

## 7. Resultados y Gráficos
El script `main_entrega3.py` genera los siguientes gráficos de análisis:
1.  **Matriz de Confusión:** Muestra la efectividad del clasificador para distinguir entre Alimentos, Limpieza e Higiene.
2.  **Importancia de Variables:** Identifica qué factores influyen más en la decisión de compra (ej. el importe suele ser determinante para la categoría).
3.  **Predicción vs Realidad (Regresión):** Un gráfico de dispersión que compara los valores reales de venta contra los predichos. Una línea diagonal perfecta indicaría un modelo perfecto.
4.  **Distribución de Importes:** Boxplot para visualizar el rango de precios y gastos por categoría.

## 8. Conclusiones
El uso de Random Forest permitió obtener modelos con alta capacidad predictiva. La separación de tareas en Clasificación y Regresión permite a la empresa no solo saber *qué* se venderá, sino *cuánto* ingreso generará esa venta.
