# --------------------------------------------------------------------
# Responde: ¿Qué tan frecuentes y qué productos compran los clientes más fieles? (clientes con más compras)
# --------------------------------------------------------------------

def analizar_clientes_fieles(df_maestro):
    # Definir un umbral para considerar a un cliente como "fiel"
    umbral_fidelidad = 5  # Por ejemplo, 5 compras

    # Contar la cantidad de compras por cliente
    df_compras_cliente = df_maestro['id_cliente'].value_counts().reset_index()
    df_compras_cliente.columns = ['id_cliente', 'cantidad_compras']

    # Filtrar clientes fieles
    df_fieles = df_compras_cliente[df_compras_cliente['cantidad_compras'] >= umbral_fidelidad]

    # Obtener los productos comprados por estos clientes
    df_productos_fieles = df_maestro[df_maestro['id_cliente'].isin(df_fieles['id_cliente'])]

    # Contar la cantidad de compras por producto
    df_productos_fieles = df_productos_fieles['id_producto'].value_counts().reset_index()
    df_productos_fieles.columns = ['id_producto', 'cantidad_compras']

    return df_fieles, df_productos_fieles

# --------------------------------------------------------------------
# Responde: ¿Qué tan frecuentes y qué productos compran los clientes más fieles? (clientes con más compras)
# --------------------------------------------------------------------
def analizar_frecuencia_productos_clientes_fieles(df_maestro):
    # Definir un umbral para considerar a un cliente como "fiel"
    umbral_fidelidad = 10  # Por ejemplo, 10 compras

    # Contar la cantidad de compras por cliente
    df_compras_cliente = df_maestro['id_cliente'].value_counts().reset_index()
    df_compras_cliente.columns = ['id_cliente', 'cantidad_compras']

    # Filtrar clientes fieles
    df_fieles = df_compras_cliente[df_compras_cliente['cantidad_compras'] >= umbral_fidelidad]

    # Obtener los productos comprados por estos clientes
    df_productos_fieles = df_maestro[df_maestro['id_cliente'].isin(df_fieles['id_cliente'])]

    # Contar la cantidad de compras por producto
    df_productos_fieles = df_productos_fieles['id_producto'].value_counts().reset_index()
    df_productos_fieles.columns = ['id_producto', 'cantidad_compras']

    return df_fieles, df_productos_fieles

# --------------------------------------------------------------------
# Responde: ¿Cuál es el cliente que más compra?   
# --------------------------------------------------------------------
def analizar_cliente_mas_comprador(df_maestro):
    # Contar la cantidad de compras por cliente
    df_compras_cliente = df_maestro['id_cliente'].value_counts().reset_index()
    df_compras_cliente.columns = ['id_cliente', 'cantidad_compras']

    # Obtener el cliente con más compras
    df_cliente_mas_comprador = df_compras_cliente[df_compras_cliente['cantidad_compras'] == df_compras_cliente['cantidad_compras'].max()]

    return df_cliente_mas_comprador

# --------------------------------------------------------------------
# Responde: ¿Cuál es la categoría de productos que tiene la mayor cantidad de productos vendidos?
# --------------------------------------------------------------------
def analizar_categoria_mas_vendida(df_maestro):
    # Agrupar por categoría y contar la cantidad de productos vendidos
    df_categoria_ventas = df_maestro.groupby('categoria')['cantidad'].sum().reset_index()

    # Obtener la categoría con más ventas
    df_categoria_mas_vendida = df_categoria_ventas[df_categoria_ventas['cantidad'] == df_categoria_ventas['cantidad'].max()]

    return df_categoria_mas_vendida