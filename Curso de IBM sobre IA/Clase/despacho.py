# Lista de pedidos (datos extraídos de la imagen)
pedidos = [
    {"ID": "O-702", "Pago": "Pendiente", "Stock": "Sí", "Destino": "Interior", "Peso": 7},
    {"ID": "O-708", "Pago": "Aprobado", "Stock": "Sí", "Destino": "Interior", "Peso": 10},
    {"ID": "O-705", "Pago": "Aprobado", "Stock": "No", "Destino": "Capital", "Peso": 2},
    {"ID": "O-701", "Pago": "Aprobado", "Stock": "Sí", "Destino": "Capital", "Peso": 3},
    {"ID": "O-703", "Pago": "Aprobado", "Stock": "Sí", "Destino": "Interior", "Peso": 8},
    {"ID": "O-707", "Pago": "Aprobado", "Stock": "Sí", "Destino": "Capital", "Peso": 6},
    {"ID": "O-704", "Pago": "Aprobado", "Stock": "Sí", "Destino": "Interior", "Peso": 12},
    {"ID": "O-706", "Pago": "Anulado", "Stock": "Sí", "Destino": "Capital", "Peso": 1}
]

def procesar_pedidos(lista_pedidos):
    """
    Procesa una lista de pedidos y calcula el recuento por estado y método de envío.
    """
    # Inicialización de contadores
    recuento_estados = {
        "Anulado": 0,
        "Pendiente": 0,
        "Enviado": 0
    }
    
    recuento_metodos_envio = {
        "Moto": 0,
        "Correo": 0,
        "Expreso": 0
    }
    
    # Bucle principal para iterar sobre cada pedido
    for pedido in lista_pedidos:
        estado_final = ""
        
        # Reglas para determinar el estado del pedido
        if pedido["Pago"] == "Anulado":
            estado_final = "Anulado"
        elif pedido["Pago"] != "Aprobado": # "Pendiente" en este caso
            estado_final = "Pendiente"
        elif pedido["Pago"] == "Aprobado":
            if pedido["Stock"] == "No":
                estado_final = "Enviado" 
            elif pedido["Stock"] == "Sí":
                estado_final = "Enviado"
                
                # Reglas para determinar el método de envío solo si el pedido está "Enviado"
                if pedido["Destino"] == "Capital" and pedido["Peso"] <= 5:
                    recuento_metodos_envio["Moto"] += 1
                elif pedido["Destino"] == "Interior" and pedido["Peso"] <= 10:
                    recuento_metodos_envio["Correo"] += 1
                else:
                    recuento_metodos_envio["Expreso"] += 1
        
        # Incrementar el contador del estado final del pedido
        recuento_estados[estado_final] += 1
        
    return recuento_estados, recuento_metodos_envio

# Ejecutar la función con los datos de los pedidos
estados, metodos_envio = procesar_pedidos(pedidos)

# Imprimir los resultados
print("📋 Recuento por estado:")
print(f"  - Anulado: {estados['Anulado']}")
print(f"  - Pendiente: {estados['Pendiente']}")
print(f"  - Enviado: {estados['Enviado']}")
print("\n🚚 Recuento por método de envío:")
print(f"  - Moto: {metodos_envio['Moto']}")
print(f"  - Correo: {metodos_envio['Correo']}")
print(f"  - Expreso: {metodos_envio['Expreso']}")