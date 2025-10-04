import pandas as pd
import numpy as np
import os

# --- CONFIGURACIÓN DE ARCHIVOS Y PARÁMETROS ---
ARCHIVOS = {
    'clientes': 'Clientes.xlsx',
    'productos': 'Productos.xlsx',
    'ventas': 'Ventas.xlsx',
    'detalle': 'Detalle_ventas.xlsx',
}

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén disponibles."""
    directorio_actual = os.getcwd()
    print(f"📁 Directorio actual: {directorio_actual}")
    print(f"📋 Archivos en el directorio:")
    
    archivos_en_directorio = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.csv'))]
    for archivo in archivos_en_directorio:
        print(f"   ✅ {archivo}")
    
    archivos_faltantes = []
    for key, archivo in ARCHIVOS.items():
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
            print(f"   ❌ FALTA: {archivo}")
        else:
            print(f"   ✅ ENCONTRADO: {archivo}")
    
    if archivos_faltantes:
        print(f"\n🚨 SOLUCIÓN PARA TU COMPAÑERA:")
        print(f"   1. Asegúrate de que estos archivos estén en la misma carpeta que main.py:")
        for archivo in archivos_faltantes:
            print(f"      - {archivo}")
        print(f"   2. O cambia el directorio de trabajo en la terminal:")
        print(f"      cd \"ruta/a/la/carpeta/con/los/archivos\"")
        return False
    
    print(f"✅ Todos los archivos están disponibles.")
    return True
MARGEN_GANANCIA_SIMULADO = 0.30 # 30% para calcular el Costo Unitario

# --------------------------------------------------------------------
# FASE 1: EXTRACCIÓN Y LIMPIEZA
# --------------------------------------------------------------------

def cargar_datos():
    dfs = {}
    print("Iniciando carga y limpieza inicial de datos...")
    
    # Verificar archivos antes de intentar cargarlos
    if not verificar_archivos():
        raise FileNotFoundError("No se pueden encontrar todos los archivos necesarios. Ver detalles arriba.")
    
    try:
        for key, ruta in ARCHIVOS.items():
            print(f"📖 Cargando {ruta}...")
            # Leer archivos Excel
            df = pd.read_excel(ruta)
            
            # Estandarizar nombres de columnas a minúsculas
            df.columns = df.columns.str.lower()
            print(f"   ✅ {ruta} cargado exitosamente ({len(df)} filas, {len(df.columns)} columnas)")
            dfs[key] = df
        
        # Corrección de nombres específicos para los Joins
        if 'fecha' in dfs['ventas'].columns:
            dfs['ventas'].rename(columns={'fecha': 'fecha_venta'}, inplace=True)
        if 'fecha_alta' in dfs['clientes'].columns:
            dfs['clientes'].rename(columns={'fecha_alta': 'fecha_registro'}, inplace=True)
        
        print("✅ Todos los archivos cargados correctamente.")
        return dfs
    except FileNotFoundError as e:
        print(f"\n🚨 ERROR DE ARCHIVO:")
        print(f"   No se pudo encontrar: {e.filename}")
        print(f"   Directorio actual: {os.getcwd()}")
        print(f"\n💡 SOLUCIONES:")
        print(f"   1. Copia todos los archivos .xlsx a la misma carpeta que main.py")
        print(f"   2. O navega al directorio correcto antes de ejecutar:")
        print(f"      cd \"ruta/donde/están/los/archivos\"")
        raise FileNotFoundError(f"Error al cargar archivo: {e}. Revisa las rutas en procesoDatos.py.")
    except Exception as e:
        print(f"\n🚨 ERROR INESPERADO:")
        print(f"   {type(e).__name__}: {e}")
        raise Exception(f"Error al procesar archivos Excel: {e}")

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
    df_maestro = pd.merge(df_maestro, dfs['clientes'], on='id_cliente', how='left', suffixes=('_venta', '_cliente'))
    
    # Merge 3: Maestro + Productos (Necesitamos categoría)
    df_maestro = pd.merge(df_maestro, dfs['productos'], on='id_producto', how='left', suffixes=('_detalle', '_productos'))
    
    # Limpiar nombres de columnas duplicadas y confusas
    df_maestro.rename(columns={
        'nombre_cliente_cliente': 'nombre_cliente',
        'nombre_producto_x': 'nombre_producto_detalle',
        'nombre_producto_y': 'nombre_producto',
        'precio_unitario_x': 'precio_unitario',
        'precio_unitario_y': 'precio_unitario_catalogo'
    }, inplace=True)
    
    print("DataFrame Maestro listo para el análisis.")
    return df_maestro