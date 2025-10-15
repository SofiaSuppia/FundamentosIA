# Importaciones de módulos con alias
import procesoDatos as pd
import analisisDatos as ad
import calendar
import os

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

    #Pregunta 3: Frecuentes y qué productos compran los clientes más fieles
    df_clientes_fieles, df_productos_fieles = ad.analizar_frecuencia_productos_clientes_fieles(df_maestro)
    print("\n--- 3. Clientes Más Frecuentes (10+ compras) ---")
    print(df_clientes_fieles.head(5))  # Mostrar solo top 5 clientes
    print("\n--- 3.1. Top 10 Productos más comprados por Clientes Fieles ---")
    print(df_productos_fieles)

    #Pregunta 4: Clientes que más productos compran
    resultado_compra = ad.analizar_cliente_mas_comprador(df_maestro)
    print("\n--- 4. Clientes que más productos compran ---")
    print(resultado_compra)
    
    # Pregunta 5: Categorías con más ventas e ingresos de cada categoría
    df_categoria_top, df_todas_categorias = ad.analizar_categoria_mas_vendida(df_maestro)
    print("\n--- 5. Categoría Más Vendida ---")
    print(df_categoria_top)
    print("\n--- 5.1. Resumen de Todas las Categorías ---")
    print(df_todas_categorias)

    # Pregunta 6: Productos Menos Rentables
    resultado_rentabilidad = ad.analizar_productos_menos_rentables(df_maestro)
    print("\n--- 6. 10 Productos Menos Rentables (Ganancia Bruta) ---")
    print(resultado_rentabilidad)
    
    # Pregunta 8: Ingresos por Ciudad
    resultado_ciudad = ad.analizar_ventas_por_ciudad_ingreso(df_maestro)
    print("\n--- 8. Distribución de Ingresos por Ciudad ---")
    print(resultado_ciudad)
    
    # Pregunta 9: volumen de ventas por ciudad
    resultado_volumen_ciudad = ad.analizar_volumen_por_ciudad_multiperiodo(df_maestro)
    print("\n--- 9. Volumen de Ventas por Ciudad ---")
    print(resultado_volumen_ciudad) 
    
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

    # Pregunta 13: Comportamiento de Compra por Períodos desde Registro
    df_promedio_monto_30d = ad.comportamiento_temprano_cliente(df_maestro)
    print("\n--- 13. Monto de compra promedio en los primeros 30 días ---")
    print(df_promedio_monto_30d)

    print("\n--- ANÁLISIS COMPLETADO EXITOSAMENTE ---")

if __name__ == "__main__":
    main()