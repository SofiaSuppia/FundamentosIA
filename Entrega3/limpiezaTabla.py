"""
Limpieza de datos para las tablas del proyecto
Aplica las siguientes transformaciones:
- Estandariza nombres de columnas (minúsculas, sin espacios, sin tildes)
- Elimina filas duplicadas
- Elimina filas con valores nulos
- Corrige tipos de datos
- Guarda los archivos limpios
"""

import pandas as pd
import unicodedata as ud
import os

def estandarizar_columnas(df):
    """
    Estandariza los nombres de columnas:
    - Convierte a minúsculas
    - Reemplaza espacios por guiones bajos
    - Elimina tildes y caracteres especiales
    """
    df.columns = (df.columns
                  .str.lower()  # convertir a minúscula
                  .str.replace(" ", "_", regex=False)  # reemplazar espacios
                  .map(lambda x: ud.normalize("NFKD", x)  # descomponer caracteres
                       .encode("ascii", "ignore")  # ignorar no-ASCII
                       .decode("latin1")  # decodificar
                       )
                  )
    return df


def limpiar_tabla(archivo, tipo_archivo):
    """    
    Parámetros:
    - archivo: nombre del archivo CSV
    - tipo_archivo: 'clientes', 'productos', 'ventas', 'detalle_ventas'
    """
    print(f"\n{'='*60}")
    print(f"Procesando: {archivo}")
    print(f"{'='*60}")
    
    # Leer el archivo
    df = pd.read_csv(archivo, encoding='utf-8')
    
    print(f"Registros originales: {len(df)}")
    print(f"Columnas originales: {list(df.columns)}")
    
    # 1. Estandarizar nombres de columnas PRIMERO
    df = estandarizar_columnas(df)
    print(f"\nColumnas estandarizadas: {list(df.columns)}")
    
    # 2. Verificar y eliminar duplicados
    duplicados_antes = df.duplicated().sum()
    if duplicados_antes > 0:
        print(f"Filas duplicadas encontradas: {duplicados_antes}")
        df = df.drop_duplicates()
        print(f"Duplicados eliminados")
    else:
        print(f"No se encontraron duplicados")
    
    # 3. Convertir columnas de texto a minúsculas (excepto IDs y números)
    columnas_texto = []
    for col in df.columns:
        if df[col].dtype == 'object' and not col.startswith('id_'):
            columnas_texto.append(col)
            # Aplicar minúsculas solo si no son nulos
            df[col] = df[col].str.lower() if df[col].notna().any() else df[col]
    
    if columnas_texto:
        print(f"Columnas convertidas a minúsculas: {columnas_texto}")
    
    # 4. Verificar valores nulos
    nulos_por_columna = df.isnull().sum()
    total_nulos = nulos_por_columna.sum()
    
    if total_nulos > 0:
        print(f"\nValores nulos encontrados:")
        for col, cant in nulos_por_columna[nulos_por_columna > 0].items():
            print(f"   - {col}: {cant} nulos")
        
        # Eliminar filas con valores nulos
        df = df.dropna()
        print(f"Filas con nulos eliminadas")
    else:
        print(f"No se encontraron valores nulos")
    
    # 5. Convertir tipos de datos específicos según el tipo de archivo
    if tipo_archivo == 'clientes':
        if 'fecha_alta' in df.columns:
            df['fecha_alta'] = pd.to_datetime(df['fecha_alta'], errors='coerce')
    
    elif tipo_archivo == 'ventas':
        if 'fecha' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            # Agregar columnas temporales para análisis (P12 - Tendencia Temporal)
            df['anio'] = df['fecha'].dt.year
            df['mes'] = df['fecha'].dt.month
            df['trimestre'] = df['fecha'].dt.quarter
            df['nombre_mes'] = df['fecha'].dt.month_name()
            print(f"✅ Columnas temporales agregadas: anio, mes, trimestre, nombre_mes")
    
    elif tipo_archivo in ['productos', 'detalle_ventas']:
        # Convertir columnas numéricas
        columnas_numericas = ['precio_unitario', 'cantidad', 'importe']
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 6. Eliminar filas que quedaron con nulos después de conversiones
    filas_despues_conversion = len(df)
    df = df.dropna()
    if len(df) < filas_despues_conversion:
        print(f"Se eliminaron {filas_despues_conversion - len(df)} filas con errores de conversión")
    
    print(f"\nRegistros finales: {len(df)}")
    print(f"Columnas finales: {len(df.columns)}")
    
    # 7. Guardar archivo limpio
    nombre_limpio = archivo.replace('.csv', '_limpio.csv')
    df.to_csv(nombre_limpio, index=False, encoding='utf-8')
    print(f"Archivo guardado: {nombre_limpio}")
    
    # 8. Mostrar resumen de tipos de datos
    print(f"\nTipos de datos finales:")
    print(df.dtypes)
    
    return df


def crear_tabla_maestra(clientes_df, ventas_df, detalle_df, productos_df):
    """
    Crea una tabla maestra combinando todas las tablas
    Esta tabla facilita responder preguntas complejas
    """
    print("\n" + "="*60)
    print("CREANDO TABLA MAESTRA")
    print("="*60)
    
    # 1. Combinar Detalle_ventas con Ventas
    maestro = detalle_df.merge(ventas_df, on='id_venta', how='left', suffixes=('', '_venta'))
    print(f"Detalle_ventas + Ventas: {len(maestro)} registros")
    
    # 2. Agregar información de Clientes
    maestro = maestro.merge(clientes_df, on='id_cliente', how='left', suffixes=('', '_cliente'))
    print(f"+ Clientes: {len(maestro)} registros")
    
    # 3. Agregar información de Productos (si no está ya)
    if 'categoria' not in maestro.columns:
        productos_mini = productos_df[['id_producto', 'categoria']].copy()
        maestro = maestro.merge(productos_mini, on='id_producto', how='left')
        print(f"+ Productos: {len(maestro)} registros")
    
    # 4. Calcular columnas derivadas importantes
    
    # Para P13 y P9: Días desde el alta del cliente hasta la compra
    if 'fecha' in maestro.columns and 'fecha_alta' in maestro.columns:
        maestro['dias_desde_alta'] = (maestro['fecha'] - maestro['fecha_alta']).dt.days
        print(f"Columna 'dias_desde_alta' agregada")
    
    # Para P2, P3, P4: Cantidad de productos por venta (ya está como 'cantidad')
    # El importe ya está calculado
    
    # Limpiar columnas duplicadas (quedarnos solo con las más relevantes)
    columnas_a_eliminar = [col for col in maestro.columns if col.endswith('_venta') or col.endswith('_cliente')]
    if columnas_a_eliminar:
        maestro = maestro.drop(columns=columnas_a_eliminar)
        print(f"Columnas duplicadas eliminadas: {len(columnas_a_eliminar)}")
    
    print(f"\nTabla maestra: {len(maestro)} registros, {len(maestro.columns)} columnas")
    print(f"Columnas: {list(maestro.columns)}")
    
    # Guardar tabla maestra
    maestro.to_csv('Tabla_Maestra_limpia.csv', index=False, encoding='utf-8')
    print(f"✅ Tabla maestra guardada: Tabla_Maestra_limpia.csv")
    
    return maestro


def main():
    print("="*60)
    print("SCRIPT DE LIMPIEZA DE DATOS")
    print("="*60)
    
    # Definir los archivos a procesar (con mayúsculas como están en el directorio)
    archivos = {
        'Clientes.csv': 'clientes',
        'Productos.csv': 'productos',
        'Ventas.csv': 'ventas',
        'Detalle_ventas.csv': 'detalle_ventas'
    }
    
    resultados = {}
    dataframes = {}  # Guardar los DataFrames limpios
    
    # Procesar cada archivo
    for archivo, tipo in archivos.items():
        if os.path.exists(archivo):
            try:
                df_limpio = limpiar_tabla(archivo, tipo)
                resultados[archivo] = {
                    'exito': True,
                    'registros': len(df_limpio),
                    'columnas': len(df_limpio.columns)
                }
                dataframes[tipo] = df_limpio  # Guardar DataFrame limpio
            except Exception as e:
                print(f"\nError procesando {archivo}: {str(e)}")
                resultados[archivo] = {
                    'exito': False,
                    'error': str(e)
                }
        else:
            print(f"\nArchivo no encontrado: {archivo}")
            resultados[archivo] = {
                'exito': False,
                'error': 'Archivo no encontrado'
            }
    
    # Crear tabla maestra si todos los archivos se procesaron correctamente
    if len(dataframes) == 4:
        try:
            tabla_maestra = crear_tabla_maestra(
                dataframes['clientes'],
                dataframes['ventas'],
                dataframes['detalle_ventas'],
                dataframes['productos']
            )
            resultados['Tabla_Maestra'] = {
                'exito': True,
                'registros': len(tabla_maestra),
                'columnas': len(tabla_maestra.columns)
            }
        except Exception as e:
            print(f"\nError creando tabla maestra: {str(e)}")
            resultados['Tabla_Maestra'] = {
                'exito': False,
                'error': str(e)
            }
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    
    for archivo, resultado in resultados.items():
        if resultado['exito']:
            print(f"{archivo}: {resultado['registros']} registros, {resultado['columnas']} columnas")
        else:
            print(f"{archivo}: {resultado.get('error', 'Error desconocido')}")
    
    print("\n" + "="*60)
    print("COLUMNAS ÚTILES PARA RESPONDER PREGUNTAS")
    print("="*60)
    print("""
📊 TABLA MAESTRA contiene todo lo necesario:
    
Para análisis de CLIENTES (P1-P4, P13):
  - id_cliente, nombre_cliente, ciudad
  - dias_desde_alta (para P13, P9)
  - importe (para calcular ingresos)
  - cantidad (para P2, P3, P14)

Para análisis de PRODUCTOS (P5-P7):
  - id_producto, nombre_producto, categoria
  - cantidad (productos vendidos)
  - importe (ingresos por producto)

Para análisis TEMPORAL (P12):
  - fecha, anio, mes, trimestre, nombre_mes
  - ciudad (para análisis por ciudad)

Para análisis de PAGO (P10, P11):
  - medio_pago
  - ciudad
  - importe

💡 CÓMO RESPONDER CADA PREGUNTA:
  P1:  GROUP BY id_cliente → SUM(importe) → Pareto 80%
  P2-P3: GROUP BY id_cliente → AVG/MIN/MAX(importe)
  P4:  GROUP BY id_cliente → SUM(importe) → MAX
  P5:  GROUP BY categoria → SUM(importe), COUNT(*)
  P6:  GROUP BY id_producto → COUNT(*) → ORDER BY ASC → TOP 10
  P7:  FILTRAR primera compra por cliente → GROUP BY producto
  P8-P9: GROUP BY ciudad → SUM(importe)
  P10-P11: GROUP BY medio_pago, ciudad → COUNT(*), AVG(importe)
  P12: GROUP BY mes/trimestre, ciudad → SUM(importe)
  P13: FILTRAR por días_desde_alta (0-30, 31-90, etc.) → Análisis
  P14: GROUP BY id_venta → AVG(cantidad), AVG(importe)
    """)
    
    print("¡Proceso de limpieza completado!")


if __name__ == "__main__":
    main()
