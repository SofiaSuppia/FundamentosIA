import pandas as pd
import numpy as np

# --------------------------------------------------------------------
# FUNCIONES DE ANÁLISIS CONTROLAR
# --------------------------------------------------------------------

def analizar_clientes_pareto(df_maestro):
    """
    Responde: ¿Quiénes son los clientes que generan el 80% de los ingresos?
    (Clientes con mayor aporte a la tienda).
    """
    
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

def analizar_productos_menos_rentables(df_maestro):
    """
    Responde: ¿Cuáles son los 10 productos menos rentables por volumen 
    y cuál es su categoría? (Usa la ganancia bruta simulada).
    """
    
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

def analizar_ventas_por_ciudad_ingreso(df_maestro):
    """
    Responde: ¿Cuál es la ciudad que genera más ingresos? ¿Cómo se distribuyen los ingresos?
    """
    
    # Usamos el Monto_Total por venta para evitar sumar detalles
    df_ventas_ciudad = df_maestro[['id_venta', 'ciudad', 'monto_total']].drop_duplicates()
    
    # Agrupar por ciudad y sumar los montos
    df_ingresos_ciudad = df_ventas_ciudad.groupby('ciudad')['monto_total'].sum().reset_index()
    
    # Calcular porcentaje sobre el total
    ingreso_total = df_ingresos_ciudad['monto_total'].sum()
    df_ingresos_ciudad['Porcentaje_Ingreso'] = (df_ingresos_ciudad['monto_total'] / ingreso_total) * 100
    
    df_ingresos_ciudad.sort_values(by='monto_total', ascending=False, inplace=True)
    
    return df_ingresos_ciudad.round(2)

# ... (Aquí irían el resto de las funciones de análisis para el resto de preguntas) ...