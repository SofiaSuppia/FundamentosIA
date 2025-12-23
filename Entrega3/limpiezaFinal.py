import pandas as pd
import numpy as np
import unicodedata as ud
import os
import re

def estandarizar_texto(texto):
    """
    Limpia el texto: minúsculas, sin tildes, sin caracteres especiales ni no imprimibles.
    """
    if pd.isna(texto): return texto
    texto = str(texto).lower().strip()
    # Eliminar tildes
    texto = ''.join(c for c in ud.normalize('NFD', texto) if ud.category(c) != 'Mn')
    # Eliminar caracteres no imprimibles y especiales (dejando solo letras, números y espacios básicos)
    texto = ''.join(c for c in texto if c.isprintable())
    # Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def estandarizar_columnas(df):
    """
    Estandariza nombres de columnas: minúsculas, sin tildes, guiones bajos.
    """
    nuevas_cols = []
    for col in df.columns:
        col_limpia = estandarizar_texto(col)
        col_limpia = col_limpia.replace(' ', '_').replace('.', '').replace('-', '_')
        nuevas_cols.append(col_limpia)
    df.columns = nuevas_cols
    return df

def extraer_contenido(nombre_prod):
    """
    Extrae la cantidad/contenido del nombre del producto (ej: 1.5l, 500g, x4).
    """
    if pd.isna(nombre_prod): return None
    nombre = str(nombre_prod).lower()
    
    # Regex para buscar patrones de cantidad
    # 1. Cantidades con unidad (1.5l, 500ml, 1kg, 250g, 20 saquitos)
    # 2. Cantidades tipo pack (x4, x100)
    # 3. Unidades sueltas si están explícitas (no común en este dataset pero útil)
    patron = r'(\d+(?:\.\d+)?\s*(?:kg|g|l|ml|cc|saquitos|sobres)|x\s*\d+)'
    
    match = re.search(patron, nombre)
    if match:
        return match.group(0).strip()
    return None

def limpiar_y_verificar():
    print("="*60)
    print("INICIANDO LIMPIEZA Y VERIFICACIÓN FINAL")
    print("="*60)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    archivos = {
        'Clientes_limpio.csv': 'clientes',
        'Productos_limpio.csv': 'productos',
        'Ventas_limpio.csv': 'ventas',
        'Detalle_ventas_limpio.csv': 'detalle'
    }
    
    for nombre_archivo, tipo in archivos.items():
        ruta = os.path.join(script_dir, nombre_archivo)
        if not os.path.exists(ruta):
            print(f"❌ Archivo no encontrado: {nombre_archivo}")
            continue
            
        print(f"\nProcesando: {nombre_archivo}")
        df = pd.read_csv(ruta)
        
        # 1. Estandarizar columnas
        df = estandarizar_columnas(df)
        
        # 2. Limpieza de texto en todas las celdas string
        cols_texto = df.select_dtypes(include=['object']).columns
        for col in cols_texto:
            df[col] = df[col].apply(estandarizar_texto)
            
        # 3. Eliminar duplicados
        duplicados = df.duplicated().sum()
        if duplicados > 0:
            df = df.drop_duplicates()
            print(f"   - Eliminados {duplicados} registros duplicados.")
        else:
            print("   - Sin duplicados.")
        # 4. Validar formatos específicos
        if tipo == 'clientes':
            # Validar emails
            if 'email' in df.columns:
                invalidos = df[~df['email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', regex=True, na=False)]
                if len(invalidos) > 0:
                    print(f"   - ⚠️ {len(invalidos)} emails con formato sospechoso.")
        
        if tipo == 'productos':
            # RE-CATEGORIZACIÓN (Desactivada para preservar categorías del usuario)
            # print("   - Actualizando categorías de productos...")
            # df['categoria'] = df['nombre_producto'].apply(asignar_categoria_producto)
            
            # Correcciones manuales específicas si 'yerba' quedó mal
            # mask_yerba = df['nombre_producto'].str.contains('yerba', na=False)
            # df.loc[mask_yerba, 'categoria'] = 'Bebidas' # Infusión
            
            # EXTRACCIÓN DE CONTENIDO
            print("   - Extrayendo contenido/cantidad...")
            df['contenido'] = df['nombre_producto'].apply(extraer_contenido)

            # Resumen de categorías
            print(f"   - Categorías resultantes: {df['categoria'].unique()}")

        # 5. Guardar
        df.to_csv(ruta, index=False)
        print(f"   ✅ Archivo guardado y limpio.")

if __name__ == "__main__":
    limpiar_y_verificar()
