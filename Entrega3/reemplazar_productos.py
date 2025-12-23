import pandas as pd
import os

# Datos proporcionados por el usuario
data = [
    [101, "Arroz Largo Fino 1kg", "Granos y Cereales", 2500],
    [102, "Fideos Tallarín 500g", "Granos y Cereales", 1800],
    [103, "Aceite de Girasol 900ml", "Aceites y Condimentos", 3200],
    [104, "Sal Fina 500g", "Aceites y Condimentos", 950],
    [105, "Atún en Lomitos 170g", "Conservas", 2900],
    [106, "Galletitas Dulces Rellenas 150g", "Snacks y Dulces", 1200],
    [107, "Papas Fritas Clásicas 120g", "Snacks y Dulces", 2100],
    [201, "Manzana Roja 1kg", "Frutas", 2200],
    [202, "Banana 1kg", "Frutas", 1900],
    [203, "Tomate Redondo 1kg", "Verduras", 2400],
    [204, "Pechuga de Pollo 1kg", "Carnes y Pescados", 5500],
    [205, "Carne de Res (Vacío) 1kg", "Carnes y Pescados", 8900],
    [301, "Leche Entera Larga Vida 1L", "Lácteos y Refrigerados", 1600],
    [302, "Yogur con Cereales 160g", "Lácteos y Refrigerados", 1450],
    [303, "Queso Rallado Reggianito 150g", "Lácteos y Refrigerados", 3100],
    [304, "Manteca Primer Calidad 200g", "Lácteos y Refrigerados", 2300],
    [401, "Pan de Molde Blanco 560g", "Panadería y Tortillería", 3400],
    [402, "Tortillas de Harina x12 unidades", "Panadería y Tortillería", 1850],
    [403, "Croissants de Manteca x6 unidades", "Panadería y Tortillería", 4200],
    [501, "Agua Mineral sin Gas 1.5L", "Bebidas", 1100],
    [502, "Gaseosa Cola 2.25L", "Bebidas", 3500],
    [503, "Café Molido Intenso 250g", "Bebidas", 5800],
    [504, "Té Negro Clásico 100 sobres", "Bebidas", 2600],
    [601, "Mix de Verduras Primavera 400g", "Congelados", 2800],
    [602, "Helado de Vainilla y Chocolate 1L", "Congelados", 4900],
    [603, "Pizza de Muzzarella Congelada 450g", "Congelados", 5200],
    [701, "Detergente Lavavajillas 500ml", "Cuidado del Hogar", 1700],
    [702, "Papel Higiénico Hoja Simple x4 rollos", "Cuidado del Hogar", 2400],
    [703, "Jabón en Polvo para Ropa 800g", "Cuidado del Hogar", 4100],
    [801, "Champú Reparación Total 400ml", "Cuidado Personal", 3600],
    [802, "Pasta Dental Protección Caries 90g", "Cuidado Personal", 1950],
    [803, "Desodorante Antitranspirante 150ml", "Cuidado Personal", 2800],
    [901, "Pañales Talle G x40 unidades", "Bebé", 12500],
    [902, "Toallitas Húmedas Bebé x50 unidades", "Bebé", 3200],
    [903, "Leche de Fórmula Etapa 1 800g", "Bebé", 15800]
]

# Crear DataFrame
df = pd.DataFrame(data, columns=["id_producto", "nombre_producto", "categoria", "precio_unitario"])

# Ruta del archivo
ruta_salida = os.path.join(os.path.dirname(__file__), "Productos_limpio.csv")

# Guardar
df.to_csv(ruta_salida, index=False)
print(f"✅ Archivo Productos_limpio.csv actualizado con {len(df)} productos.")
