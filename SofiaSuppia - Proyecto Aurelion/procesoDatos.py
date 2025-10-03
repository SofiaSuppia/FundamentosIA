import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE ARCHIVOS Y PARÁMETROS ---
# NOTA: Usamos los nombres de los archivos CSV que el sistema generó
# a partir de tus archivos Excel. Si tienes los XLSX originales, podrías
# cambiar las rutas a "Clientes.xlsx", etc., y usar la hoja (sheet) si fuera necesario.
ARCHIVOS = {
    'clientes': 'Clientes - clientes.csv.csv',
    'productos': 'Copia de Productos - productos.csv.csv',
    'ventas': 'Ventas - ventas.csv.csv',
    'detalle': 'Detalle_ventas - detalle_ventas.csv.csv',
}
MARGEN_GANANCIA_SIMULADO = 0.30 # 30% para calcular el Costo Unitario

# --------------------------------------------------------------------
# FASE 1: EXTRACCIÓN Y LIMPIEZA
# --------------------------------------------------------------------

def cargar_datos():
    
    dfs = {}
    print("Iniciando carga y limpieza inicial de datos...")
    try:
        for key, ruta in ARCHIVOS.items():
            # Si los archivos fueran XLSX puros, la línea sería:
            # df = pd.read_excel(ruta, sheet_name='Hoja1') 
            
            df = pd.read_csv(ruta)
            
            # Estandarizar nombres de columnas a minúsculas
            df.columns = df.columns.str.lower()
            dfs[key] = df
        
        # Corrección de nombres específicos para los Joins
        dfs['ventas'].rename(columns={'fecha': 'fecha_venta'}, inplace=True)
        dfs['clientes'].rename(columns={'fecha_alta': 'fecha_registro'}, inplace=True)
        
        return dfs
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Error al cargar archivo: {e}. Revisa las rutas en data_processor.py.")

def generar_campos_calculados(dfs):
    """Aplica formato y genera las columnas calculadas cruciales: costo_unitario y Monto_Total."""
    
    # 1. DETALLE_VENTAS: COSTO Y GANANCIA
    df_detalle = dfs['detalle']
    factor_costo = 1 + MARGEN_GANANCIA_SIMULADO
    
    # Simulación del Costo Unitario
    df_detalle['costo_unitario'] = df_detalle['precio_unitario'] / factor_costo
    df_detalle['costo_unitario'] = df_detalle['costo_unitario'].round(2)
    
    # Cálculo de Ganancia Bruta (Ingreso - Costo)
    costo_total_linea = df_detalle['costo_unitario'] * df_detalle['cantidad']
    df_detalle['ganancia_bruta'] = df_detalle['importe'] - costo_total_linea
    
    # 2. TRATAMIENTO DE VENTAS: MONTO_TOTAL
    df_ventas = dfs['ventas']
    
    # Sumar el importe de la tabla Detalle_Ventas
    df_suma_ventas = df_detalle.groupby('id_venta')['importe'].sum().reset_index()
    df_suma_ventas.rename(columns={'importe': 'monto_total'}, inplace=True)
    
    # Unir el Monto Total a la tabla Ventas
    df_ventas = pd.merge(df_ventas, df_suma_ventas, on='id_venta', how='left')
    
    # Aplicar formato de fecha
    dfs['clientes']['fecha_registro'] = pd.to_datetime(dfs['clientes']['fecha_registro'], errors='coerce')
    df_ventas['fecha_venta'] = pd.to_datetime(df_ventas['fecha_venta'], errors='coerce')
    
    dfs['detalle'] = df_detalle
    dfs['ventas'] = df_ventas
    return dfs

def crear_df_maestro(dfs):
    """Realiza los Joins para crear el DataFrame único de análisis."""
    
    print("Creando DataFrame Maestro (Joins)...")
    
    # Merge 1: Detalle + Ventas
    df_maestro = pd.merge(dfs['detalle'], dfs['ventas'], on='id_venta', how='left', suffixes=('_detalle', '_venta'))
    
    # Merge 2: Maestro + Clientes (Necesitamos ciudad, fecha_registro, y nombre del cliente)
    df_maestro = pd.merge(df_maestro, dfs['clientes'][['id_cliente', 'ciudad', 'fecha_registro', 'nombre_cliente']], on='id_cliente', how='left', suffixes=('_venta', '_cliente'))
    
    # Merge 3: Maestro + Productos (Necesitamos categoría)
    df_maestro = pd.merge(df_maestro, dfs['productos'][['id_producto', 'categoria']], on='id_producto', how='left')
    
    # Corrección de nombres de columnas duplicadas
    df_maestro.rename(columns={'nombre_producto_detalle': 'nombre_producto'}, inplace=True)
    
    print("DataFrame Maestro listo para el análisis.")
    return df_maestro