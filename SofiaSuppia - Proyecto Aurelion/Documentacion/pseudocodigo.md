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

FUNCION ANALIZAR_MEDIOS_DE_PAGO(DF_MAESTRO):

    # 1. CUENTA LA FRECUENCIA  DE VENTAS POR MEDIO DE PAGO
    Dentro de DF_MAESTRO se cuentan los valores de la columna 'medio_pago'

    # 2. Calcula el PORCENTAJE GLOBAL de CADA MEDIO de pago
   Valores de columna 'medio_pago' en porcentaje %

    # 3. Crea los Resultados en TABLA
    Col. 1 El conteo de transacciones
    Col. 2 El porcentaje redondeado a 2 decimales

FUNCION ANALIZAR_VENTAS_POR_CIUDAD(DF_MAESTRO)

     # 1.  CONTAR VENTAS POR COMBINANCION ('ciudad' y 'medio_pago')
     CONTEO_DOBLE = AGRUPAR por DF_MAESTRO .CONTAR_FILAS() Reiniciar indice (nombre = 'conteo_ventas' )

    # 2. CALCULAR EL TOTAL DE VENTAS POR CADA CIUDAD
       TOTAL_POR_CIUDAD = AGRUPAR POR (conteo_doble,'ciudad')
       SUMAR('conteo_ventas')
       Reiniciar indice (nombre = total_ventas_ciudad)

    # 3. UNIR EL CONTEO ESPECIFICO CON EL TOTAL DE LA CIUDAD
        DF_RESULTADO = conteo_doble UNION 'total_ventas_ciudad'

    # 4. CALCULAR EL PORCENTAJE POR CIUDAD
     CREA columna Porcentaje ciudad = con 'conteo_ventas / Total_ventas_ciudad' 

    # 5. FORMATEAR Y DEVOLVER EL RESULTADO
    -REDONDEA el resultado
    -DEVUELVE las COLUMNAS 'ciudad', medio_pago' y 'porcentaje ciudad'


FUNCION ANALISIS_TEMPORAL_MAYOR_INGRESO(DF_MAESTRO):
    # 1. AGRUPAR por ''id_venta' y SUMAR 'importe'
    CREA columna 'monto_total_venta' con suma total

    # 2.  LIMPIA datos
    EXTRAER 'id_venta' y 'fecha_venta' sin duplicados
    UNIR 'monto_total_venta' con 'fecha_venta' usando 'id_venta'

    # 3.  Columnas temporales 
    df_analisis_temporal =
        CREA columna 'mes_nombre' a partir de 'fecha_venta'
        CREA columna 'trimestre' a partir de  'fecha_venta'

    # 4. ANALISIS POR MES
        df_importe_por_mes = AGRUPA POR MES Y SUMA 'monto_total_venta'

    # 5.ANALISIS POR TRIMESTRE
        df_importe_por_trimestre = AGRUPA POR TRIMESTRE Y SUMA 'monto_total_venta'

    # 6. FORMATEA Y DEVUELVE 
    Resultados por monto descendente

FUNCION COMPORTAMIENTO TEMPRANO DEL CLIENTE

    # 1. IMPORTE DE VENTAS POR TRANSACCION
     df_monto_total_venta = AGRUPA por 'id_venta'.SUMA 'importe' y CONVIERTE indice
     df_monto_total_venta = RENOMBRA la columna 'importe' a 'monto_total_venta'

    # 2. EXTRAER COLUMNAS RELEVANTES POR VENTA
    df_info_venta = df_maestro COLUMNAS ''id_venta', 'id_cliente', 'fecha', 'fecha_alta' SIN DUPLICADOS

    # 3. UNIR MONTO TOTAL CON INFO DE VENTA
    df_ventas_completas = df_ monto_total_venta (ex 'importe') UNIR con df_info_venta a IZQUIERDA

    # 4. RESTA FECHAS Y APLICA FILTRO DE 30D
    CREA COLUMNA 'primeros_30d' = 'fecha' - ''fecha_alta' en FORMATO DIAS
    FILTRO <=30 DIAS

    # 5. CALCULO PROMEDIO DE MONTO TOTAL
    df_promedio_monto_30d = df_filtrado_30d en COLUMNA 'monto_total' PROMEDIO y REDONDEO


FUNCION ANALISIS_CATEGORIA_MAYOR_INGRESO(DF_MAESTRO):
    df_categorias = AGRUPA POR CATEGORIA Y SUMA 'ganancia_bruta'
    
    df_mayor_ingreso = ORDENAR df_categorias DESCENDENTE POR 'Ganancia_Total'
    -DEVUELVE LAS COLUMNAS 'categoria' Y 'Ganancia_Total'

FUNCION ANALISIS_CATEGORIA_MAYOR_CANTIDAD_DE_VENTAS(DF_MAESTRO):
    df_categorias = AGRUPA POR CATEGORIA Y SUMA 'cantidad'
    
    df_mayor_cantidad_de_unidades = ORDENAR df_categorias DESCENDENTE POR 'Unidades_Vendidas'
    -DEVUELVE LAS COLUMNAS 'categoria' Y 'Unidades_Vendidas'


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