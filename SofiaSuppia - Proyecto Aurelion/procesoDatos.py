import pandas as pd
import numpy as np
import os
import calendar

# --- CONFIGURACIÓN DE ARCHIVOS Y PARÁMETROS ---
ARCHIVOS = {
    'clientes': 'Clientes.xlsx',
    'productos': 'Productos.xlsx',
    'ventas': 'Ventas.xlsx',
    'detalle': 'Detalle_ventas.xlsx',
}

# Posibles ubicaciones donde buscar los archivos
RUTAS_POSIBLES = [
    '.',  # Directorio actual
    './BaseDatos',  # Subdirectorio BaseDatos
    '../BaseDatos',  # BaseDatos en directorio padre
    './SofiaSuppia - Proyecto Aurelion/BaseDatos',  # Ruta relativa completa
]

def buscar_archivos():
    """Busca los archivos en diferentes ubicaciones posibles."""
    for ruta_base in RUTAS_POSIBLES:
        if os.path.exists(ruta_base):
            archivos_encontrados = {}
            todos_encontrados = True
            
            for key, archivo in ARCHIVOS.items():
                ruta_completa = os.path.join(ruta_base, archivo)
                if os.path.exists(ruta_completa):
                    archivos_encontrados[key] = ruta_completa
                else:
                    todos_encontrados = False
                    break
            
            if todos_encontrados:
                return archivos_encontrados
    
    return None

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén disponibles."""
    directorio_actual = os.getcwd()
    
    # Buscar archivos en ubicaciones posibles
    archivos_encontrados = buscar_archivos()
    
    if archivos_encontrados:
        return archivos_encontrados
    
    # Si no se encontraron, mostrar diagnóstico
    print(f"📋 Archivos en el directorio actual:")
    try:
        archivos_en_directorio = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.csv'))]
        if archivos_en_directorio:
            for archivo in archivos_en_directorio:
                print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ No hay archivos .xlsx o .csv en este directorio")
    except Exception as e:
        print(f"   ❌ Error al listar directorio: {e}")
    
    # Verificar subdirectorios
    print(f"\n📂 Buscando en subdirectorios...")
    for ruta in RUTAS_POSIBLES[1:]:  # Excluir directorio actual
        if os.path.exists(ruta):
            try:
                archivos_subdir = [f for f in os.listdir(ruta) if f.endswith(('.xlsx', '.csv'))]
                if archivos_subdir:
                    print(f"   📁 {ruta}:")
                    for archivo in archivos_subdir:
                        print(f"      ✅ {archivo}")
                else:
                    print(f"   📁 {ruta}: (vacío)")
            except Exception as e:
                print(f"   📁 {ruta}: Error - {e}")
        else:
            print(f"   📁 {ruta}: (no existe)")
    
    print(f"\n🚨 SOLUCIÓN:")
    print(f"   1. Copia estos archivos al directorio actual ({directorio_actual}):")
    for archivo in ARCHIVOS.values():
        print(f"      - {archivo}")
    print(f"   2. O crea una carpeta 'BaseDatos' y ponlos ahí")
    print(f"   3. O navega al directorio donde están los archivos:")
    print(f"      cd \"ruta/donde/están/los/archivos\"")
    
    return None
MARGEN_GANANCIA_SIMULADO = 0.30 # 30% para calcular el Costo Unitario

# --------------------------------------------------------------------
# FASE 1: EXTRACCIÓN Y LIMPIEZA
# --------------------------------------------------------------------

def cargar_datos():
    dfs = {}
    
    # Verificar y buscar archivos en diferentes ubicaciones
    archivos_encontrados = verificar_archivos()
    if not archivos_encontrados:
        raise FileNotFoundError("No se pueden encontrar todos los archivos necesarios. Ver detalles arriba.")
    
    try:
        for key, ruta_completa in archivos_encontrados.items():
            # Leer archivos Excel
            df = pd.read_excel(ruta_completa)
            
            # Estandarizar nombres de columnas a minúsculas
            df.columns = df.columns.str.lower()
            dfs[key] = df
        
        # Corrección de nombres específicos para los Joins
        if 'fecha' in dfs['ventas'].columns:
            dfs['ventas'].rename(columns={'fecha': 'fecha_venta'}, inplace=True)
        if 'fecha_alta' in dfs['clientes'].columns:
            dfs['clientes'].rename(columns={'fecha_alta': 'fecha_registro'}, inplace=True)
        
        return dfs
    except FileNotFoundError as e:
        print(f"\n🚨 ERROR DE ARCHIVO:")
        print(f"   No se pudo encontrar: {e.filename}")
        print(f"   Directorio actual: {os.getcwd()}")
        print(f"\n💡 SOLUCIONES:")
        print(f"   1. Copia todos los archivos .xlsx a la misma carpeta que main.py")
        print(f"   2. O crea una carpeta 'BaseDatos' y ponlos ahí")
        print(f"   3. O navega al directorio correcto antes de ejecutar:")
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
    
    return df_maestro