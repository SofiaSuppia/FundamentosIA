import time

def mostrar_titulo():
    """Imprime el título principal del proyecto."""
    print("="*60)
    print("🚀 Proyecto Aurelion - Sistema de Análisis de Ventas 🚀")
    print("="*60)
    print("Autor: Sofia Suppia")
    print("Fecha: Octubre 2025")
    print("Materia: Fundamentos de Inteligencia Artificial\n")
    time.sleep(1)

def mostrar_resumen():
    """Muestra la sección de resumen del proyecto."""
    print("\n--- 🎯 Resumen ---")
    print("\n[Tema Principal]")
    print("Análisis de datos de ventas en un market digital para identificar patrones, optimizar decisiones y diseñar estrategias de fidelización.")
    
    print("\n[Problema Identificado]")
    print("La empresa carece de un sistema para responder preguntas estratégicas clave,")
    print("lo que impide la toma de decisiones basadas en datos.")
    
    print("\n[Solución Propuesta]")
    print("Desarrollo de un programa en Python que integra y analiza múltiples fuentes de datos")
    print("utilizando Pandas para generar insights valiosos.")
    time.sleep(1)

def mostrar_analisis_problema():
    """Describe el contexto y los objetivos del problema."""
    print("\n--- 🔍 Análisis del Problema ---")
    print("\n[Contexto Empresarial]")
    print("Simulación del análisis de datos para una tienda digital que necesita optimizar operaciones.")
    
    print("\n[Objetivos Específicos]")
    objetivos = [
        "1. Identificación de clientes estratégicos (Análisis Pareto 80/20).",
        "2. Optimización del inventario mediante análisis de productos.",
        "3. Análisis de rentabilidad geográfica por ciudades.",
        "4. Evaluación de métodos de pago preferidos."
    ]
    for objetivo in objetivos:
        print(f"- {objetivo}")
        time.sleep(0.5)

def mostrar_arquitectura_datos():
    """Presenta la estructura y origen de los datos."""
    print("\n--- 💾 Arquitectura de Datos ---")
    print("\n[Origen de los Datos]")
    print("Simulación de ventas históricas estructuradas en cuatro archivos Excel.")
    
    print("\n[Estructura de la Base de Datos]")
    tablas = {
        "Clientes": "ID, Nombre, Ciudad, Fecha_Registro",
        "Productos": "ID, Nombre, Categoría",
        "Ventas": "ID_Venta, ID_Cliente, Fecha, Medio_Pago, Monto",
        "Detalle_Ventas": "Cantidad, Precios, Costos, Importe"
    }
    print("Tablas principales:")
    for tabla, campos in tablas.items():
        print(f"  - {tabla}: ({campos})")
        time.sleep(0.5)

def mostrar_preguntas_estrategicas():
    """Enumera las preguntas estratégicas que el sistema busca responder."""
    print("\n--- ❓ Preguntas Estratégicas ---")
    preguntas = {
        "Análisis de Clientes": [
            "¿Quiénes son los clientes que generan el 80% de los ingresos?",
            "¿Cuál es el valor de compra promedio, mínimo y máximo?",
            "¿Qué tan frecuentes son las compras de los clientes más fieles?"
        ],
        "Análisis de Productos": [
            "¿Qué categorías de productos son las más rentables?",
            "¿Cuáles son los 10 productos menos vendidos?",
            "¿Qué productos se compran más en el primer pedido?"
        ],
        "Análisis Geográfico": [
            "¿Cómo se distribuyen los ingresos entre las ciudades?",
            "¿Cuál es el volumen de ventas promedio por ciudad en los primeros 30 días?"
        ]
    }
    for categoria, lista_preguntas in preguntas.items():
        print(f"\n[{categoria}]")
        for i, pregunta in enumerate(lista_preguntas, 1):
            print(f"  {i}. {pregunta}")
            time.sleep(0.3)

def mostrar_stack_tecnologico():
    """Muestra las tecnologías utilizadas en el proyecto."""
    print("\n--- 🔧 Implementación Técnica ---")
    print("\n[Stack Tecnológico]")
    stack = {
        "Python 3.8+": "Lenguaje principal para la lógica de negocio.",
        "Pandas": "Para manipulación y análisis de datos (DataFrames).",
        "NumPy": "Para cálculos numéricos eficientes.",
        "Openpyxl": "Para la lectura de archivos Excel (.xlsx)."
    }
    for herramienta, proposito in stack.items():
        print(f"  - {herramienta}: {proposito}")
        time.sleep(0.5)

def main():
    """Función principal que orquesta la presentación del proyecto."""
    mostrar_titulo()
    
    opciones = {
        "1": ("Resumen", mostrar_resumen),
        "2": ("Análisis del Problema", mostrar_analisis_problema),
        "3": ("Arquitectura de Datos", mostrar_arquitectura_datos),
        "4": ("Preguntas Estratégicas", mostrar_preguntas_estrategicas),
        "5": ("Stack Tecnológico", mostrar_stack_tecnologico),
        "6": ("Mostrar Todo", None),
        "7": ("Salir", None)
    }

    while True:
        print("\n" + "="*25)
        print("Menú de Información")
        print("="*25)
        for key, (value, _) in opciones.items():
            print(f"{key}. {value}")
        
        eleccion = input("\nSelecciona una opción para ver los detalles: ")

        if eleccion == "7":
            print("¡Hasta luego!")
            break
        elif eleccion == "6":
            mostrar_resumen()
            mostrar_analisis_problema()
            mostrar_arquitectura_datos()
            mostrar_preguntas_estrategicas()
            mostrar_stack_tecnologico()
            print("\n--- Fin de la presentación completa ---")
        elif eleccion in opciones:
            _, funcion = opciones[eleccion]
            funcion()
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
