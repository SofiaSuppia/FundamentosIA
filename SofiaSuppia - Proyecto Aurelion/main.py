# Importaciones de módulos con alias
import procesoDatos as pd
import analisisDatos as ad
import calendar

def main():
    print("--- INICIO DEL ANÁLISIS DE VENTAS ---")

    # 1. EXTRACCIÓN Y PREPARACIÓN
    try:
        # Carga los archivos y aplica limpieza inicial
        dfs = pd.cargar_datos()
        
        # Genera los campos calculados (Costo Unitario y Monto Total)
        dfs = pd.generar_campos_calculados(dfs)
    except FileNotFoundError as e:
        print(f"\n¡ERROR! El programa no encuentra los archivos. Revisa que estén en la misma carpeta que main.py. Detalle: {e}")
        return
    except Exception as e:
        print(f"\n¡ERROR CRÍTICO EN PREPARACIÓN DE DATOS! {e}")
        return

    # 2. CREACIÓN DEL DATAFRAME MAESTRO
    df_maestro = pd.crear_df_maestro(dfs)

    # 3. EJECUCIÓN DEL ANÁLISIS ESTRATÉGICO
    print("\n\n=======================================================")
    print("               RESULTADOS DEL ANÁLISIS")
    print("=======================================================")

    # Pregunta 1: Clientes Pareto (Top 80% de Ingresos)
    resultado_pareto = ad.analizar_clientes_pareto(df_maestro)
    print("\n--- 1. Clientes Pareto (Top 80% de Ingresos) ---")
    print(resultado_pareto)
    
    # Pregunta 2: Promedio, Mínimo y Máximo de Compra
    resultado_valor_compra = ad.analizar_valor_promedio_compra(df_maestro)
    print("\n--- 2. Promedio, Mínimo y Máximo de Compra ---")
    print(resultado_valor_compra)

    # Pregunta 6: Productos Menos Rentables
    resultado_rentabilidad = ad.analizar_productos_menos_rentables(df_maestro)
    print("\n--- 6. 10 Productos Menos Rentables (Ganancia Bruta) ---")
    print(resultado_rentabilidad)

    #Pregunta 7: Productos mas vendidos en la primera compra 
    

    
    # Pregunta 8: Ingresos por Ciudad
    resultado_ciudad = ad.analizar_ventas_por_ciudad_ingreso(df_maestro)
    print("\n--- 8. Distribución de Ingresos por Ciudad ---")
    print(resultado_ciudad)
    
    # Pregunta 10: Análisis de Medios de Pago (Porcentaje)
    df_porcentaje_global = ad.analizar_medios_de_pago(df_maestro)
    print("\n--- 10. Distribución de Medios de pago ---")
    print(df_porcentaje_global)

    # Pregunta 10.2: Análisis de medios de pago por Ciudad
    df_resultado_porcentaje = ad.analizar_ventas_por_ciudad_pago(df_maestro)
    print("\n--- 10.2. Porcentaje de Medios de pago por Ciudad ---")
    print(df_resultado_porcentaje)
    
    # Pregunta 11: Promedio de Medios de pago por Venta
    df_promedio = ad.promedio_de_medio_de_pago(df_maestro)
    print("\n--- 11. Monto Promedio de Venta por Medio de Pago ---")
    print(df_promedio)

    # Pregunta 12: Mes y trimestre con más ingresos
    df_importe_por_mes, df_importe_por_trimestre = ad.analisis_temporal_mayor_ingreso(df_maestro)

    print("\n--- 12. Importe Total de Ventas por Mes ---")
    print(df_importe_por_mes)

    print("\n--- 12.2 Importe Total de Ventas por Trimestre ---")
    print(df_importe_por_trimestre)

    # Pregunta 13: Categoria con mayor ingreso

    print("\n--- 13.1 Categoria con mayor ingreso total ---")
    df_categoria_mayor_ingreso = ad.analisis_categoria_mayor_ingreso(df_maestro)
    print(df_categoria_mayor_ingreso)

    print("\n--- 13.2 Categoria con mayor cantidad de unidades vendidas ---")
    df_categoria_mayor_cantidades_vendidas = ad.analisis_categoria_mayor_cantidad_de_ventas(df_maestro)
    print(df_categoria_mayor_cantidades_vendidas)
    # Pregunta 13: Comportamiento Temprano del Cliente (30D)
    df_promedio_monto_30d = ad.comportamiento_temprano_cliente(df_maestro)
    print("\n--- 13. Monto de compra promedio en los primeros 30 días ---")
    print(df_promedio_monto_30d)

    # ... (Llamadas a las demás funciones de análisis) ...

    print("\n--- ANÁLISIS COMPLETADO EXITOSAMENTE ---")

if __name__ == "__main__":
    main()