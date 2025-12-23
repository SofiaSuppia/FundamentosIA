import pandas as pd
import os

# Definir rutas
base_path = 'Entrega3'
productos_path = os.path.join(base_path, 'Productos_limpio.csv')
clientes_path = os.path.join(base_path, 'Clientes_limpio.csv')
ventas_path = os.path.join(base_path, 'Ventas_limpio.csv')
detalle_path = os.path.join(base_path, 'Detalle_ventas_limpio.csv')

# Cargar datos
print("Cargando archivos...")
df_productos = pd.read_csv(productos_path)
df_clientes = pd.read_csv(clientes_path)
df_ventas = pd.read_csv(ventas_path)
df_detalle = pd.read_csv(detalle_path)

# --- Análisis de Productos ---
print("\n--- ANÁLISIS DE PRODUCTOS ---")
todos_productos = set(df_productos['id_producto'])
productos_vendidos = set(df_detalle['id_producto'])

productos_sin_ventas = todos_productos - productos_vendidos
total_productos = len(todos_productos)
cant_sin_ventas = len(productos_sin_ventas)

print(f"Total de productos en tabla maestra: {total_productos}")
print(f"Total de productos distintos vendidos: {len(productos_vendidos)}")
print(f"Cantidad de productos SIN ventas: {cant_sin_ventas}")

if cant_sin_ventas > 0:
    print("IDs de productos sin ventas:", sorted(list(productos_sin_ventas)))
    # Verificar si los nuevos (asumiendo ID > 100) están en esta lista
    nuevos_sin_ventas = [p for p in productos_sin_ventas if p > 100]
    if nuevos_sin_ventas:
        print(f"¡ATENCIÓN! Hay {len(nuevos_sin_ventas)} productos NUEVOS (ID > 100) que no se han vendido nunca.")
        print("IDs nuevos sin ventas:", sorted(nuevos_sin_ventas))
    else:
        print("Todos los productos nuevos (ID > 100) registran al menos una venta.")
else:
    print("¡Éxito! Todos los productos han sido vendidos al menos una vez.")

# --- Análisis de Clientes ---
print("\n--- ANÁLISIS DE CLIENTES ---")
todos_clientes = set(df_clientes['id_cliente'])
clientes_con_compras = set(df_ventas['id_cliente'])

clientes_sin_compras = todos_clientes - clientes_con_compras
total_clientes = len(todos_clientes)
cant_sin_compras = len(clientes_sin_compras)

print(f"Total de clientes en tabla maestra: {total_clientes}")
print(f"Total de clientes distintos con compras: {len(clientes_con_compras)}")
print(f"Cantidad de clientes SIN compras: {cant_sin_compras}")

if cant_sin_compras > 0:
    print("IDs de clientes sin compras:", sorted(list(clientes_sin_compras)))
    # Verificar si hay muchos clientes sin compras
    porcentaje_sin_compra = (cant_sin_compras / total_clientes) * 100
    print(f"Porcentaje de clientes inactivos: {porcentaje_sin_compra:.2f}%")
else:
    print("¡Éxito! Todos los clientes han realizado al menos una compra.")
