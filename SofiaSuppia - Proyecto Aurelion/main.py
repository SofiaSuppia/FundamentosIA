from procesoDatos import cargar_datos, generar_campos_calculados, crear_df_maestro
from analisisDatos import analizar_clientes_pareto, analizar_productos_menos_rentables, analizar_ventas_por_ciudad_ingreso

def main():
    print("--- INICIO DEL ANÁLISIS DE VENTAS ---")

    # 1. EXTRACCIÓN Y PREPARACIÓN
    try:
        # Carga los archivos y aplica limpieza inicial
        dfs = cargar_datos()
        
        # Genera los campos calculados (Costo Unitario y Monto Total)
        dfs = generar_campos_calculados(dfs)
    except FileNotFoundError as e:
        print(f"\n¡ERROR! El programa no encuentra los archivos. Revisa que estén en la misma carpeta que main.py. Detalle: {e}")
        return
    except Exception as e:
        print(f"\n¡ERROR CRÍTICO EN PREPARACIÓN DE DATOS! {e}")
        return

    # 2. CREACIÓN DEL DATAFRAME MAESTRO
    df_maestro = crear_df_maestro(dfs)

    # 3. EJECUCIÓN DEL ANÁLISIS ESTRATÉGICO
    print("\n\n=======================================================")
    print("               RESULTADOS DEL ANÁLISIS")
    print("=======================================================")

    # Pregunta 1: Clientes Pareto (Top 80% de Ingresos)
    resultado_pareto = analizar_clientes_pareto(df_maestro)
    print("\n--- 1. Clientes Pareto (Top 80% de Ingresos) ---")
    print(resultado_pareto)

    # Pregunta 2: Productos Menos Rentables
    resultado_rentabilidad = analizar_productos_menos_rentables(df_maestro)
    print("\n--- 2. 10 Productos Menos Rentables (Ganancia Bruta) ---")
    print(resultado_rentabilidad)
    
    # Pregunta 3: Ingresos por Ciudad
    resultado_ciudad = analizar_ventas_por_ciudad_ingreso(df_maestro)
    print("\n--- 3. Distribución de Ingresos por Ciudad ---")
    print(resultado_ciudad)
    
    # ... (Llamadas a las demás funciones de análisis) ...

    print("\n--- ANÁLISIS COMPLETADO EXITOSAMENTE ---")

if __name__ == "__main__":
    main()