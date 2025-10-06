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

    return df_resultado[['nombre_cliente', 'monto_total', 'pct_acumulado']].head(10)

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
    
    return df_resultado.round(2)

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

    return df_menos_rentables[['nombre_producto_detalle', 'categoria', 'Ganancia_Total', 'Unidades_Vendidas']]

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
    
    return df_ingresos_ciudad.round(2)

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

    return df_resultado_porcentaje

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

    # Formateo el resultado
    df_promedio['Monto Promedio de Venta'] = df_promedio['Monto Promedio de Venta'].round(2)
    df_promedio.sort_values(by='Monto Promedio de Venta', ascending=False, inplace=True)

    return df_promedio

#-------