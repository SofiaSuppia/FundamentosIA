# procesoDatos.py

DEFINIR MARGEN_GANANCIA = 0.30
DEFINIR LISTA DE RUTAS_ARCHIVOS

FUNCION CARGAR_DATOS():
    PARA CADA ruta EN LISTA DE RUTAS_ARCHIVOS:
        LEER archivo CSV usando Pandas (pd.read_csv)
        ESTANDARIZAR nombres de columnas a minúsculas
        ALMACENAR en diccionario de DataFrames (DFS)
    RENOMBRAR columnas clave (ej: fecha en Ventas a 'fecha_venta')
    DEVOLVER DFS

FUNCION GENERAR_CAMPOS_CALCULADOS(DFS):
    
    # 1. CÁLCULO DE RENTABILIDAD (Detalle_Ventas)
    DF_DETALLE = DFS['detalle']
    FACTOR = 1 + MARGEN_GANANCIA  # 1.30
    
    # Cálculo del Costo Unitario Simulado
    DF_DETALLE['costo_unitario'] = DF_DETALLE['precio_unitario'] / FACTOR
    
    # Cálculo de Ganancia Bruta (Ingreso - Costo)
    COSTO_TOTAL_LINEA = DF_DETALLE['costo_unitario'] * DF_DETALLE['cantidad']
    DF_DETALLE['ganancia_bruta'] = DF_DETALLE['importe'] - COSTO_TOTAL_LINEA
    
    # 2. CÁLCULO DE MONTO_TOTAL (Ventas)
    DF_SUMA_VENTAS = AGRUPAR DF_DETALLE POR 'id_venta'
                     SUMAR 'importe' COMO 'monto_total'
    
    # Agregar Monto_Total a la tabla Ventas
    DF_VENTAS = UNIR DFS['ventas'] CON DF_SUMA_VENTAS POR 'id_venta' (Merge Left)
    
    # 3. FORMATO DE FECHAS
    CONVERTIR columna 'fecha_registro' (Clientes) a formato Fecha
    CONVERTIR columna 'fecha_venta' (Ventas) a formato Fecha
    
    DEVOLVER DFS actualizado

FUNCION CREAR_DF_MAESTRO(DFS):
    
    # 1. Unir Detalle y Ventas (Base de la Transacción)
    DF_MAESTRO = UNIR DFS['detalle'] CON DFS['ventas'] POR 'id_venta'
    
    # 2. Unir Clientes (Añadir ciudad y nombre_cliente)
    DF_MAESTRO = UNIR DF_MAESTRO CON DFS['clientes'] POR 'id_cliente'
    
    # 3. Unir Productos (Añadir categoría)
    DF_MAESTRO = UNIR DF_MAESTRO CON DFS['productos'] POR 'id_producto'
    
    DEVOLVER DF_MAESTRO


------------------------------------------------------------------------------------------------------------------------------------------------

# analysis_manager.py

FUNCION ANALIZAR_CLIENTES_PARETO(DF_MAESTRO):
    
    # 1. Calcular Ingreso Total por Cliente
    DF_INGRESOS = AGRUPAR DF_MAESTRO POR 'id_cliente' (usando solo ventas únicas)
                  SUMAR 'monto_total'
    
    # 2. Clasificar Pareto
    ORDENAR DF_INGRESOS DESCENDENTE por 'monto_total'
    CALCULAR 'ingreso_acumulado'
    CALCULAR 'pct_acumulado' = 'ingreso_acumulado' / SUMA_TOTAL_GLOBAL
    
    # 3. Devolver Top 10 Clientes que alcanzan el 80%
    FILTRAR DF_PARETO DONDE 'pct_acumulado' <= 0.80
    DEVOLVER Top 10 de DF_PARETO

FUNCION ANALIZAR_PRODUCTOS_MENOS_RENTABLES(DF_MAESTRO):
    
    # 1. Agrupar Rentabilidad por Producto
    DF_RENTABILIDAD = AGRUPAR DF_MAESTRO POR 'id_producto', 'nombre_producto', 'categoria'
                      SUMAR 'ganancia_bruta' COMO 'Ganancia_Total'
                      SUMAR 'cantidad' COMO 'Unidades_Vendidas'

    # 2. Identificar Menos Rentables
    ORDENAR DF_RENTABILIDAD ASCENDENTE por 'Ganancia_Total'
    
    # 3. Devolver Top 10
    DEVOLVER Top 10 de DF_RENTABILIDAD (los menos rentables)

FUNCION ANALIZAR_VENTAS_POR_CIUDAD(DF_MAESTRO):
    
    # 1. Calcular Ingreso Total por Ciudad
    DF_INGRESOS_CIUDAD = AGRUPAR DF_MAESTRO POR 'ciudad' (usando solo ventas únicas)
                         SUMAR 'monto_total'
    
    # 2. Calcular Porcentaje y Ordenar
    CALCULAR 'Porcentaje_Ingreso'
    ORDENAR DF_INGRESOS_CIUDAD DESCENDENTE por 'monto_total'
    
    DEVOLVER DF_INGRESOS_CIUDAD

# ... (Se añadirían FUNCIONES para el resto de las preguntas estratégicas) ...

---------------------------------------------------------------------------------------------------------------------------------------------

# main.py

IMPORTAR FUNCIONES de data_processor
IMPORTAR FUNCIONES de analysis_manager

FUNCION PRINCIPAL():
    IMPRIMIR "INICIO DEL PROCESO ETL"

    # FASE 1: EXTRACCIÓN Y TRANSFORMACIÓN
    DFS = LLAMAR CARGAR_DATOS()
    SI HAY ERROR DE ARCHIVO ENTONCES TERMINAR
    
    DFS = LLAMAR GENERAR_CAMPOS_CALCULADOS(DFS)
    DF_MAESTRO = LLAMAR CREAR_DF_MAESTRO(DFS)

    IMPRIMIR "DATAFRAME MAESTRO CREADO. INICIO ANÁLISIS."

    # FASE 2: ANÁLISIS ESTRATÉGICO
    
    # Pregunta 1: Clientes Pareto
    RESULTADO_PARETO = LLAMAR ANALIZAR_CLIENTES_PARETO(DF_MAESTRO)
    IMPRIMIR "RESULTADOS PARETO:"
    IMPRIMIR RESULTADO_PARETO
    
    # Pregunta 2: Productos Menos Rentables
    RESULTADO_RENTABILIDAD = LLAMAR ANALIZAR_PRODUCTOS_MENOS_RENTABLES(DF_MAESTRO)
    IMPRIMIR "RESULTADOS RENTABILIDAD:"
    IMPRIMIR RESULTADO_RENTABILIDAD
    
    # Pregunta 3: Ingresos por Ciudad
    RESULTADO_CIUDAD = LLAMAR ANALIZAR_VENTAS_POR_CIUDAD(DF_MAESTRO)
    IMPRIMIR "RESULTADOS POR CIUDAD:"
    IMPRIMIR RESULTADO_CIUDAD
    
    # ... (Llamadas a las demás funciones de análisis) ...
    
    IMPRIMIR "PROCESO COMPLETADO EXITOSAMENTE"

EJECUTAR FUNCION PRINCIPAL SI ES EL ARCHIVO DE ARRANQUE