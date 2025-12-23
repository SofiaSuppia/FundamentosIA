import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import os

# --- FUNCIONES AUXILIARES DE AMPLIACIÓN ---
def ampliar_clientes(df_clientes, n_nuevos):
    # Limpiar clientes sintéticos anteriores para reemplazarlos con nombres reales
    df_clientes = df_clientes[~df_clientes['nombre_cliente'].str.contains("Cliente_Sintetico", na=False)]
    
    if n_nuevos <= 0: return df_clientes
    
    print(f"   + Generando {n_nuevos} clientes nuevos con nombres realistas...")
    last_id = df_clientes['id_cliente'].max()
    if pd.isna(last_id): last_id = 0
    ciudades = df_clientes['ciudad'].unique()
    
    # Listas de nombres y apellidos
    nombres = [
        'Sofía', 'Valentina', 'María José', 'Ximena', 'Regina', 'María Carmen',
        'Mateo', 'Santiago', 'Sebastián', 'Alejandro', 'Antonio'
    ]
    apellidos = [
        'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez', 'Pérez',
        'Gómez', 'Díaz', 'Romero', 'Hernández', 'Cruz', 'Flores', 'Torres', 'Morales', 'Ramírez',
        'Reyes', 'Ramos', 'Ruiz', 'Castro', 'Castillo'
    ]
    
    nuevos = []
    for i in range(n_nuevos):
        nuevo_id = last_id + i + 1
        nombre = np.random.choice(nombres)
        apellido = np.random.choice(apellidos)
        nombre_completo = f"{nombre} {apellido}"
        
        # Generar email limpio (sin tildes ni espacios)
        def clean(t): return t.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')
        email = f"{clean(nombre).replace(' ', '.')}.{clean(apellido)}@mail.com"
        
        # Fecha sin hora
        fecha_alta = pd.Timestamp('2024-01-01') + pd.to_timedelta(np.random.randint(0, 365), unit='D')
        
        nuevos.append({
            'id_cliente': nuevo_id,
            'nombre_cliente': nombre_completo,
            'email': email,
            'ciudad': np.random.choice(ciudades),
            'fecha_alta': fecha_alta.strftime('%Y-%m-%d')
        })
    
    return pd.concat([df_clientes, pd.DataFrame(nuevos)], ignore_index=True)

def ampliar_productos(df_productos, n_nuevos):
    # 1. Eliminar productos sintéticos anteriores ("Producto_Nuevo_X")
    df_productos = df_productos[~df_productos['nombre_producto'].str.contains("Producto_Nuevo", na=False)]
    
    print(f"   + Generando productos nuevos realistas...")
    
    # Diccionario de nuevos productos con sus categorías
    nuevos_items = {
        'Conservas': ['Atún en lata', 'Chiles en lata', 'Lentejas en lata', 'Garbanzos en lata'],
        'Snacks y Dulces': ['Galletas dulces', 'Galletas saladas', 'Papas fritas', 'Gelatina en polvo', 'Barra de cereal'],
        'Frutas': ['Manzana', 'Banana', 'Naranja', 'Uvas', 'Kiwi', 'Fresas'],
        'Verduras': ['Tomate', 'Lechuga', 'Zanahoria', 'Papa', 'Cebolla', 'Brócoli', 'Pimiento'],
        'Carnes y Pescados': ['Corte de res', 'Pollo entero', 'Filete de pescado', 'Mariscos surtidos', 'Chuleta de cerdo'],
        'Lácteos': ['Leche entera', 'Leche descremada', 'Leche vegetal', 'Yogur bebible', 'Queso rallado', 'Manteca'],
        'Panadería': ['Pan de molde', 'Baguette', 'Tortillas de maíz', 'Pan dulce', 'Croissants', 'Facturas'],
        'Bebidas': ['Agua embotellada', 'Refresco cola', 'Jugo de naranja', 'Café molido', 'Té negro', 'Bebida energética'],
        'Congelados': ['Verduras congeladas', 'Helado de crema', 'Hamburguesas congeladas', 'Pizza congelada'],
        'Cuidado del Hogar': ['Detergente ropa', 'Lavavajillas', 'Limpiador multiuso', 'Papel higiénico', 'Bolsas de basura'],
        'Cuidado Personal': ['Jabón de tocador', 'Shampoo', 'Acondicionador', 'Pasta dental', 'Desodorante'],
        'Bebé': ['Pañales', 'Toallitas húmedas', 'Leche de fórmula', 'Papilla de frutas']
    }

    last_id = df_productos['id_producto'].max()
    if pd.isna(last_id): last_id = 0
    
    nuevos_registros = []
    count = 0
    
    for categoria, items in nuevos_items.items():
        for item in items:
            # Verificar si ya existe para no duplicar
            if item in df_productos['nombre_producto'].values:
                continue
                
            count += 1
            nuevo_id = last_id + count
            
            # Precio aleatorio entre 500 y 15000
            precio = np.random.randint(500, 15000)
            
            nuevos_registros.append({
                'id_producto': nuevo_id,
                'nombre_producto': item,
                'categoria': categoria,
                'precio_unitario': precio
            })
            
    if nuevos_registros:
        return pd.concat([df_productos, pd.DataFrame(nuevos_registros)], ignore_index=True)
    return df_productos

# --- PASO 1: AMPLIACIÓN FÍSICA DE LAS TABLAS ---
def ampliar_tablas_csv(n_nuevas_ventas=2000, n_nuevos_clientes=50, n_nuevos_productos=20):
    """
    Genera nuevas ventas, las relaciona con datos existentes y actualiza los archivos CSV.
    """
    print(f"🔄 Iniciando ampliación física de las tablas (+{n_nuevas_ventas} registros)...")
    
    # Obtener directorio del script para usar rutas absolutas
    script_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        # Cargar tablas base
        path_clientes = os.path.join(script_dir, 'Clientes_limpio.csv')
        path_productos = os.path.join(script_dir, 'Productos_limpio.csv')
        
        df_clientes = pd.read_csv(path_clientes)
        df_productos = pd.read_csv(path_productos)
        
        # --- NUEVO: Ampliar Clientes y Productos ---
        df_clientes = ampliar_clientes(df_clientes, n_nuevos_clientes)
        df_productos = ampliar_productos(df_productos, n_nuevos_productos)
        
        # Guardar los cambios en Clientes y Productos
        df_clientes.to_csv(path_clientes, index=False)
        df_productos.to_csv(path_productos, index=False)
        
        # Rutas de archivos de ventas
        path_ventas = os.path.join(script_dir, 'Ventas_limpio.csv')
        path_detalle = os.path.join(script_dir, 'Detalle_ventas_limpio.csv')

        # Cargar tablas de transacciones actuales (o crearlas si no existen)
        if os.path.exists(path_ventas):
            df_ventas = pd.read_csv(path_ventas)
            
            # --- LIMPIEZA DE REGISTROS ANTERIORES ---
            # 1. Limpiar registros incompletos
            df_ventas = df_ventas.dropna(subset=['nombre_cliente'])
            # 2. Limpiar ventas de clientes sintéticos antiguos para regenerarlas con nombres reales
            df_ventas = df_ventas[~df_ventas['nombre_cliente'].str.contains("Cliente_Sintetico", na=False)]
            
            last_id_venta = df_ventas['id_venta'].max()
            if pd.isna(last_id_venta): last_id_venta = 0
        else:
            df_ventas = pd.DataFrame(columns=['id_venta', 'id_cliente', 'fecha', 'medio_pago', 'monto_total'])
            last_id_venta = 0

        if os.path.exists(path_detalle):
            df_detalle = pd.read_csv(path_detalle)
            # Sincronizar: Eliminar detalles de ventas que ya no existen (por la limpieza de ventas)
            df_detalle = df_detalle[df_detalle['id_venta'].isin(df_ventas['id_venta'])]
            # Sincronizar: Eliminar detalles de productos que ya no existen (por la limpieza de productos)
            df_detalle = df_detalle[df_detalle['id_producto'].isin(df_productos['id_producto'])]
        else:
            df_detalle = pd.DataFrame(columns=['id_venta', 'id_producto', 'nombre_producto', 'cantidad', 'precio_unitario', 'importe'])

    except FileNotFoundError:
        print("❌ Error: Faltan archivos base. Asegúrate de ejecutar limpiezaTabla.py primero.")
        return None

    nuevas_filas_ventas = []
    nuevas_filas_detalle = []
    medios_pago = ['efectivo', 'tarjeta_debito', 'tarjeta_credito', 'transferencia']
    fechas = pd.date_range(start='2024-01-01', end='2024-12-31').astype(str)

    for i in range(n_nuevas_ventas):
        current_id_venta = last_id_venta + i + 1
        
        # 1. Seleccionar Cliente y Producto aleatorio para mantener relación
        cliente = df_clientes.sample(1).iloc[0]
        producto = df_productos.sample(1).iloc[0]
        
        cantidad = np.random.randint(1, 6)
        precio = producto['precio_unitario']
        importe_total = cantidad * precio
        
        # Calcular datos temporales
        fecha_str = np.random.choice(fechas)
        fecha_dt = pd.to_datetime(fecha_str)
        
        # 2. Crear registro para tabla Ventas (COMPLETO)
        venta_reg = {
            'id_venta': current_id_venta,
            'fecha': fecha_str,
            'id_cliente': cliente['id_cliente'],
            'nombre_cliente': cliente['nombre_cliente'],
            'email': cliente['email'],
            'medio_pago': np.random.choice(medios_pago),
            'anio': fecha_dt.year,
            'mes': fecha_dt.month,
            'trimestre': fecha_dt.quarter,
            'nombre_mes': fecha_dt.month_name(),
            'monto_total': importe_total
        }
        nuevas_filas_ventas.append(venta_reg)
        
        # 3. Crear registro para tabla Detalle_Ventas
        detalle_reg = {
            'id_venta': current_id_venta,
            'id_producto': producto['id_producto'],
            'nombre_producto': producto['nombre_producto'],
            'cantidad': cantidad,
            'precio_unitario': precio,
            'importe': importe_total
        }
        nuevas_filas_detalle.append(detalle_reg)

    # 4. Concatenar y guardar
    df_ventas_actualizado = pd.concat([df_ventas, pd.DataFrame(nuevas_filas_ventas)], ignore_index=True)
    df_detalle_actualizado = pd.concat([df_detalle, pd.DataFrame(nuevas_filas_detalle)], ignore_index=True)
    
    df_ventas_actualizado.to_csv(path_ventas, index=False)
    df_detalle_actualizado.to_csv(path_detalle, index=False)
    
    print(f"✅ Tablas actualizadas. Ventas totales ahora: {len(df_ventas_actualizado)}")
    return df_ventas_actualizado, df_detalle_actualizado, df_clientes, df_productos

# --- PASO 2: CONSTRUCCIÓN DEL DATAFRAME MAESTRO PARA ML ---
def generar_dataset_maestro(df_v, df_d, df_c, df_p):
    """
    Une las 4 tablas ampliadas en un solo DataFrame para el entrenamiento.
    """
    # Unir Detalle con Productos
    m1 = pd.merge(df_d, df_p[['id_producto', 'categoria']], on='id_producto')
    # Unir con Ventas
    m2 = pd.merge(m1, df_v[['id_venta', 'id_cliente', 'medio_pago', 'fecha']], on='id_venta')
    # Unir con Clientes
    maestro = pd.merge(m2, df_c[['id_cliente', 'ciudad']], on='id_cliente')
    
    # Extraer el mes de la fecha
    maestro['fecha'] = pd.to_datetime(maestro['fecha'])
    maestro['mes'] = maestro['fecha'].dt.month
    maestro['trimestre'] = maestro['fecha'].dt.quarter
    
    return maestro

# --- PASO 3: PREPROCESAMIENTO Y ML ---
def entrenar_modelo_ia():
    # 1. Ampliar y cargar datos desde CSVs
    resultado = ampliar_tablas_csv(2000)
    if resultado is None: return
    
    df_v, df_d, df_c, df_p = resultado
    
    # 2. Generar el dataset de entrenamiento unificado
    df_maestro = generar_dataset_maestro(df_v, df_d, df_c, df_p)
    
    # 3. Codificación
    le_ciudad = LabelEncoder()
    le_pago = LabelEncoder()
    le_cat = LabelEncoder()
    
    df_maestro['ciudad_n'] = le_ciudad.fit_transform(df_maestro['ciudad'])
    df_maestro['pago_n'] = le_pago.fit_transform(df_maestro['medio_pago'])
    df_maestro['target'] = le_cat.fit_transform(df_maestro['categoria'])
    
    # 4. Variables X e y (Agregamos trimestre)
    X = df_maestro[['ciudad_n', 'pago_n', 'cantidad', 'importe', 'mes', 'trimestre']]
    y = df_maestro['target']
    
    # 5. Entrenamiento
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("🧠 Entrenando modelo optimizado (Random Forest)...")
    # Aumentamos estimadores y ajustamos profundidad para mejorar precisión
    modelo = RandomForestClassifier(n_estimators=300, max_depth=20, min_samples_split=5, random_state=42)
    modelo.fit(X_train, y_train)
    
    y_pred = modelo.predict(X_test)
    
    # 6. Métricas
    print("\n📊 RESULTADOS DEL MODELO")
    print(f"Precisión: {accuracy_score(y_test, y_pred):.2f}")
    print(classification_report(y_test, y_pred, target_names=le_cat.classes_))
    
    # 7. Gráficos
    visualizar_resultados(modelo, X.columns, y_test, y_pred, le_cat.classes_)

def visualizar_resultados(modelo, features, y_test, y_pred, clases):
    # Importancia de Variables
    plt.figure(figsize=(10, 5))
    sns.barplot(x=modelo.feature_importances_, y=features, palette='viridis')
    plt.title('Variables clave para la predicción')
    plt.show()

    # Matriz de Confusión
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=clases, yticklabels=clases)
    plt.title('Matriz de Confusión')
    plt.ylabel('Real')
    plt.xlabel('Predicho')
    plt.show()

if __name__ == "__main__":
    entrenar_modelo_ia()