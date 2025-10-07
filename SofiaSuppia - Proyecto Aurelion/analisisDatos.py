import pandas as pd
import numpy as np

# --------------------------------------------------------------------
# FUNCIONES DE ANÁLISIS CONTROLAR
# --------------------------------------------------------------------

# --------------------------------------------------------------------
# Responde: ¿Quiénes son los clientes que generan el 80% de los ingresos? (Clientes con mayor aporte a la tienda)
# --------------------------------------------------------------------

def analizar_clientes_pareto(df_maestro):
    # Agrupar por cliente y sumar el Monto_Total (usamos drop_duplicates ya que Monto_Total se repite por detalle)
    df_ventas_cliente = df_maestro[['id_venta', 'id_cliente', 'monto_total']].drop_duplicates()
    df_ingresos = df_ventas_cliente.groupby('id_cliente')['monto_total'].sum().reset_index()
    
    # Ordenar y calcular el porcentaje acumulado
    df_ingresos.sort_values(by='monto_total', ascending=False, inplace=True)
    ingreso_total = df_ingresos['monto_total'].sum()
    
    df_ingresos['ingreso_acumulado'] = df_ingresos['monto_total'].cumsum()
    df_ingresos['pct_acumulado'] = df_ingresos['ingreso_acumulado'] / ingreso_total
    
    # Filtrar el top 80%
    df_pareto = df_ingresos[df_ingresos['pct_acumulado'] <= 0.80]
    
    # Unir con el nombre del cliente para el resultado
    df_resultado = pd.merge(df_pareto, df_maestro[['id_cliente', 'nombre_cliente']].drop_duplicates(), on='id_cliente', how='left')

    return df_resultado[['nombre_cliente', 'monto_total', 'pct_acumulado']].head(10).reset_index(drop=True)

# --------------------------------------------------------------------
# Responde: ¿Cuál es el promedio, mínimo y máximo de compra de nuestros clientes?
# --------------------------------------------------------------------
def analizar_valor_promedio_compra(df_maestro):
    # Agrupar por cliente y sumar el Monto_Total (usamos drop_duplicates ya que Monto_Total se repite por detalle)
    df_ventas_cliente = df_maestro[['id_venta', 'id_cliente', 'monto_total']].drop_duplicates()
    df_ingresos = df_ventas_cliente.groupby('id_cliente')['monto_total'].sum().reset_index()
    
    # Calcular promedio, mínimo y máximo
    promedio_compra = df_ingresos['monto_total'].mean()
    minimo_compra = df_ingresos['monto_total'].min()
    maximo_compra = df_ingresos['monto_total'].max()
    
    # Crear un DataFrame para el resultado
    df_resultado = pd.DataFrame({
        'Promedio de Compra': [promedio_compra],
        'Mínimo de Compra': [minimo_compra],
        'Máximo de Compra': [maximo_compra]
    })
    
    return df_resultado.round(2).reset_index(drop=True)

# --------------------------------------------------------------------
# Responde: ¿Qué tan frecuentes y qué productos compran los clientes más fieles?
# --------------------------------------------------------------------
def analizar_frecuencia_productos_clientes_fieles(df_maestro):
    # Definir un umbral para considerar a un cliente como "fiel"
    umbral_fidelidad = 10  # Por ejemplo, 10 compras

    # Contar la cantidad de compras por cliente
    df_compras_cliente = df_maestro['id_cliente'].value_counts().reset_index()
    df_compras_cliente.columns = ['id_cliente', 'cantidad_compras']

    # Filtrar clientes fieles
    df_fieles = df_compras_cliente[df_compras_cliente['cantidad_compras'] >= umbral_fidelidad]
    
    # Agregar nombres de clientes fieles
    df_fieles_con_nombres = df_fieles.merge(
        df_maestro[['id_cliente', 'nombre_cliente']].drop_duplicates(), 
        on='id_cliente', 
        how='left'
    )
    
    # Ordenar por cantidad de compras (descendente)
    df_fieles_con_nombres = df_fieles_con_nombres.sort_values('cantidad_compras', ascending=False)

    # Obtener los productos comprados por estos clientes fieles
    df_productos_fieles = df_maestro[df_maestro['id_cliente'].isin(df_fieles['id_cliente'])]

    # Contar la cantidad de veces que se compra cada producto
    df_productos_frecuencia = df_productos_fieles['id_producto'].value_counts().reset_index()
    df_productos_frecuencia.columns = ['id_producto', 'frecuencia_compra']
    
    # Agregar nombres de productos y categorías
    df_productos_con_nombres = df_productos_frecuencia.merge(
        df_maestro[['id_producto', 'nombre_producto_detalle', 'categoria']].drop_duplicates(),
        on='id_producto',
        how='left'
    )
    
    # Calcular también la cantidad total vendida de cada producto a clientes fieles
    df_cantidad_productos = df_productos_fieles.groupby(['id_producto', 'nombre_producto_detalle', 'categoria']).agg(
        cantidad_total_vendida=('cantidad', 'sum'),
        frecuencia_compra=('id_producto', 'count')
    ).reset_index()
    
    # Ordenar por frecuencia de compra (descendente)
    df_cantidad_productos = df_cantidad_productos.sort_values('frecuencia_compra', ascending=False)

    return df_fieles_con_nombres[['nombre_cliente', 'cantidad_compras']].reset_index(drop=True), df_cantidad_productos[['nombre_producto_detalle', 'categoria', 'frecuencia_compra', 'cantidad_total_vendida']].head(10).reset_index(drop=True)

# --------------------------------------------------------------------
# Responde: ¿Cuál es el cliente que más compra?
# --------------------------------------------------------------------
def analizar_cliente_mas_comprador(df_maestro):
    # Contar la cantidad de compras por cliente
    df_compras_cliente = df_maestro['id_cliente'].value_counts().reset_index()
    df_compras_cliente.columns = ['id_cliente', 'cantidad_compras']

    # Obtener el cliente con más compras
    df_cliente_mas_comprador = df_compras_cliente[df_compras_cliente['cantidad_compras'] == df_compras_cliente['cantidad_compras'].max()]
    
    # Agregar el nombre del cliente
    df_resultado = df_cliente_mas_comprador.merge(
        df_maestro[['id_cliente', 'nombre_cliente']].drop_duplicates(), 
        on='id_cliente', 
        how='left'
    )

    return df_resultado[['nombre_cliente', 'id_cliente', 'cantidad_compras']].reset_index(drop=True)

# --------------------------------------------------------------------
# Responde: ¿Cuál es la categoría de productos que tiene la mayor cantidad de productos vendidos?
# ¿Me podes decir los ingresos de cada categoría?
# --------------------------------------------------------------------
def analizar_categoria_mas_vendida(df_maestro):
    # Agrupar por categoría y calcular tanto cantidad vendida como ingresos
    df_categoria_analisis = df_maestro.groupby('categoria').agg({
        'cantidad': 'sum',
        'ganancia_bruta': 'sum',
        'importe': 'sum'
    }).reset_index()
    
    # Renombrar columnas para mayor claridad
    df_categoria_analisis.columns = ['categoria', 'cantidad_total_vendida', 'ganancia_total', 'ingresos_totales']
    
    # Ordenar por cantidad vendida (descendente) para ver todas las categorías
    df_categoria_analisis = df_categoria_analisis.sort_values('cantidad_total_vendida', ascending=False)
    
    # Obtener la categoría con más ventas (primera fila después del ordenamiento)
    df_categoria_mas_vendida = df_categoria_analisis.head(1)
    
    # Formatear números para mejor presentación
    df_categoria_analisis = df_categoria_analisis.round(2)
    df_categoria_mas_vendida = df_categoria_mas_vendida.round(2)

    return df_categoria_mas_vendida.reset_index(drop=True), df_categoria_analisis.reset_index(drop=True)


# --------------------------------------------------------------------
# Responde: ¿Cuáles son los 10 productos menos rentables por volumen y cuál es su categoría? (Usa la ganancia bruta simulada).
# --------------------------------------------------------------------
def analizar_productos_menos_rentables(df_maestro):
    
    # Agrupar por producto y sumar la ganancia bruta y la cantidad
    df_rentabilidad = df_maestro.groupby(['id_producto', 'nombre_producto_detalle', 'categoria']).agg(
        Ganancia_Total=('ganancia_bruta', 'sum'),
        Unidades_Vendidas=('cantidad', 'sum')
    ).reset_index()
    
    # Calcular la Ganancia Promedio por Unidad para desempate
    df_rentabilidad['Ganancia_Unidad_Promedio'] = df_rentabilidad['Ganancia_Total'] / df_rentabilidad['Unidades_Vendidas']
    
    # Ordenar por Ganancia Total y Ganancia por Unidad (ambas de forma ascendente)
    df_menos_rentables = df_rentabilidad.sort_values(
        by=['Ganancia_Total', 'Ganancia_Unidad_Promedio'], 
        ascending=[True, True]
    ).head(10)

    return df_menos_rentables[['nombre_producto_detalle', 'categoria', 'Ganancia_Total', 'Unidades_Vendidas']].reset_index(drop=True)

# --------------------------------------------------------------------
#  Responde: ¿Cuál es la ciudad que genera más ingresos? ¿Cómo se distribuyen los ingresos?
# --------------------------------------------------------------------

def analizar_ventas_por_ciudad_ingreso(df_maestro):  
    # Usamos el Monto_Total por venta para evitar sumar detalles
    df_ventas_ciudad = df_maestro[['id_venta', 'ciudad', 'monto_total']].drop_duplicates()
    
    # Agrupar por ciudad y sumar los montos
    df_ingresos_ciudad = df_ventas_ciudad.groupby('ciudad')['monto_total'].sum().reset_index()
    
    # Calcular porcentaje sobre el total
    ingreso_total = df_ingresos_ciudad['monto_total'].sum()
    df_ingresos_ciudad['Porcentaje_Ingreso'] = (df_ingresos_ciudad['monto_total'] / ingreso_total) * 100
    
    df_ingresos_ciudad.sort_values(by='monto_total', ascending=False, inplace=True)
    
    return df_ingresos_ciudad.round(2).reset_index(drop=True)

# --------------------------------------------------------------------
# FUNCIONES DE ANÁLISIS CONTROLAR
# --------------------------------------------------------------------

# ... (Aquí irían el resto de las funciones de análisis para el resto de preguntas) ...


#----Fio---
# --------------------------------------------------------------------
# Responde a : ¿Cuál es el porcentaje de ventas por medio de pago ? ¿Varía este porcentaje según la ciudad?
# --------------------------------------------------------------------

def analizar_medios_de_pago(df_maestro):
    # Conteo de ventas por medio de pago (frecuencia)
    conteo_gral = df_maestro['medio_pago'].value_counts()
    
    # Cálculo el porcentaje general
    porcentaje_gral = (conteo_gral / conteo_gral.sum()) * 100

    # Combinamos los resultados 
    df_porcentaje_global = pd.DataFrame({
        'Total ventas (N)': conteo_gral,
        'Porcentaje (%)' : porcentaje_gral.round(2)
    }).sort_values(by='Porcentaje (%)', ascending=False)

    return df_porcentaje_global

def analizar_ventas_por_ciudad_pago(df_maestro):
    # Contamos el nro de filas para 'ciudad' y 'medio_pago'
    conteo_doble = df_maestro.groupby(['ciudad', 'medio_pago']).size().reset_index(name='conteo_ventas')
    
    # Calculamos el total de ventas por Ciudad
    total_por_ciudad = conteo_doble.groupby('ciudad')['conteo_ventas'].sum().reset_index(name ='total_ventas_ciudad')

    # Aplico merge para el conteo total de cada ciudad 
    df_resultado_porcentaje = conteo_doble.merge(total_por_ciudad, on ='ciudad', how='left')

    # Calculamos/ creamos columna 'Porcentaje ciudad'
    df_resultado_porcentaje['Porcentaje ciudad'] = df_resultado_porcentaje['conteo_ventas'] / df_resultado_porcentaje['total_ventas_ciudad']

    df_resultado_porcentaje['Porcentaje ciudad'] = df_resultado_porcentaje['Porcentaje ciudad'].round(2)
    df_resultado_porcentaje = df_resultado_porcentaje[['ciudad', 'medio_pago', 'Porcentaje ciudad']]

    return df_resultado_porcentaje.reset_index(drop=True)

# --------------------------------------------------------------------
# Responde a : ¿Cuál es el promedio de ventas por Medio de pago?
# --------------------------------------------------------------------
def promedio_de_medio_de_pago(df_maestro):
    # Sumamos el importe total de Ventas y agrupamos por transacción
    df_monto_total_venta = df_maestro.groupby('id_venta')['importe'].sum().reset_index()
    df_monto_total_venta.rename(columns={'importe': 'monto_total_venta'}, inplace=True)

    # Unimos el Monto total con el Medio de pago, haciendo una copia del original
    df_pago_por_venta = df_maestro[['id_venta', 'medio_pago']].drop_duplicates()

    # Unimos el monto total con SU medio de pago
    df_analisis = df_monto_total_venta.merge(df_pago_por_venta, on='id_venta', how='left')

    # Agrupamos por medio de pago y Calculamos el promedio
    df_promedio = df_analisis.groupby('medio_pago')['monto_total_venta'].mean().reset_index()

    # Renombro la columna anterior
    df_promedio.rename(columns={'monto_total_venta': 'Monto Promedio de Venta'}, inplace=True)

    # Formateo resultado
    df_promedio['Monto Promedio de Venta'] = df_promedio['Monto Promedio de Venta'].round(2)
    df_promedio.sort_values(by='Monto Promedio de Venta', ascending=False, inplace=True)

    return df_promedio.reset_index(drop=True)

# --------------------------------------------------------------------
# Responde a : ¿Cuál es el mes o trimestre con más ingresos?
# --------------------------------------------------------------------
def analisis_temporal_mayor_ingreso(df_maestro):
    # Importe de ventas por 'id_venta' transaccion
    df_monto_total_venta = df_maestro.groupby('id_venta')['importe'].sum().reset_index()
    df_monto_total_venta.rename(columns={'importe': 'monto_total_venta'}, inplace= True)

    # Unimos el Monto Total con la Fecha, evitando duplicados
    df_fechas_venta =df_maestro[['id_venta', 'fecha_venta']].drop_duplicates()
    df_analisis_temporal = df_monto_total_venta.merge(df_fechas_venta, on='id_venta' ,how='left')

    # Columna temporal de nombre de mes 
    df_analisis_temporal['mes_nombre'] = df_analisis_temporal['fecha_venta'].dt.month_name()
    df_analisis_temporal['trimestre'] = df_analisis_temporal['fecha_venta'].dt.quarter

    # Analisis por mes
    df_importe_por_mes = df_analisis_temporal.groupby('mes_nombre')['monto_total_venta'].sum().reset_index()

    # Analisis por trimestre
    df_importe_por_trimestre = df_analisis_temporal.groupby('trimestre')['monto_total_venta'].sum().reset_index()

    # Formateo resultado
    df_importe_por_mes = df_importe_por_mes.sort_values(by='monto_total_venta', ascending=False)
    df_importe_por_trimestre = df_importe_por_trimestre.sort_values(by='monto_total_venta', ascending=False)

    return df_importe_por_mes.reset_index(drop=True), df_importe_por_trimestre.reset_index(drop=True)

# --------------------------------------------------------------------
# Responde a: ¿Cuál es el comportamiento de compra de los clientes por períodos después de registrarse?
# Analiza: 30 días, 90 días, 6 meses, 1 año
# --------------------------------------------------------------------
def comportamiento_temprano_cliente(df_maestro):

    # Importe de ventas por transaccion
    df_monto_total_venta = df_maestro.groupby('id_venta')['importe'].sum().reset_index()
    df_monto_total_venta.rename(columns={'importe': 'monto_total_venta'}, inplace=True)

    # Extraer columnas relevantes por venta (sin duplicados)
    # Usar los nombres técnicos correctos que existen en el DataFrame
    df_info_venta = df_maestro[['id_venta', 'id_cliente', 'fecha_venta', 'fecha_registro']].drop_duplicates()

    # Unir Monto total con info de venta
    df_ventas_completas = df_monto_total_venta.merge(df_info_venta, on='id_venta', how='left')

    # Calcular diferencia de días entre fecha de venta y fecha de registro
    df_ventas_completas['dias_desde_registro'] = (df_ventas_completas['fecha_venta'] - df_ventas_completas['fecha_registro']).dt.days
    
    # Definir períodos para análisis
    periodos = {
        '30 días': 30,
        '90 días': 90,
        '6 meses': 180,
        '1 año': 365
    }
    
    resultados = []
    
    for nombre_periodo, dias in periodos.items():
        df_filtrado = df_ventas_completas[df_ventas_completas['dias_desde_registro'] <= dias]
        
        if len(df_filtrado) > 0:
            promedio_monto = df_filtrado['monto_total_venta'].mean().round(2)
            num_ventas = len(df_filtrado)
            num_clientes = df_filtrado['id_cliente'].nunique()
        else:
            promedio_monto = 0
            num_ventas = 0
            num_clientes = 0
            
        resultados.append({
            'Período': nombre_periodo,
            'Promedio Monto': promedio_monto,
            'Número Ventas': num_ventas,
            'Clientes Únicos': num_clientes
        })
    
    # Crear DataFrame con todos los resultados
    df_resultado = pd.DataFrame(resultados)
    
    # Agregar información adicional sobre el comportamiento general
    tiempo_promedio_primera_compra = df_ventas_completas['dias_desde_registro'].min()
    
    print(f"📊 INSIGHT: El tiempo mínimo desde registro hasta primera compra es {tiempo_promedio_primera_compra} días")
    
    return df_resultado.reset_index(drop=True)

    # Calculo de promedio de Monto Total
    df_promedio_monto_30d = df_filtrado_30d['monto_total_venta'].mean().round(2)

    return df_promedio_monto_30d