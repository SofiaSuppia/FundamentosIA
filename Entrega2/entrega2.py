import time
import textwrap
import pandas as pd
from scipy import stats
import os

def mostrar_titulo():
    """Imprime el título principal del proyecto."""
    print("="*60)
    print("🚀 Proyecto Aurelion - Sistema de Análisis de Ventas 🚀")
    print("="*60)
    print("Autor: Sofia Suppia")
    print("Fecha: Octubre 2025")
    print("Materia: Fundamentos de Inteligencia Artificial\n")
    time.sleep(1)


def mostrar_analisis_problema():
    """Describe el contexto y los objetivos del problema."""
    print("\n--- 🔍 Análisis del Problema ---")
    print("\n[Contexto Empresarial]")
    print("El Proyecto Aurelion aborda el desafío central que enfrentan las cadenas de mini súper con presencia en múltiples ciudades:")
    texto_original = """La falta de una visión unificada y analítica de la rentabilidad que permita optimizar la operación y la experiencia del cliente en cada ubicación. Actualmente, la empresa genera un gran volumen de datos de ventas, pero carece de un sistema automatizado para convertir estos datos en información estratégica y accionable. Esta ceguera analítica impide:

    1. Optimizar la Rentabilidad Geográfica:
       No se sabe con certeza qué ciudades, clientes o categorías de productos están impulsando realmente las ganancias.

    2. Personalizar la Atención y Fidelización:
       Es imposible identificar y recompensar a los clientes más valiosos, ni entender su comportamiento de compra a lo largo del tiempo.

    3. Mejorar la Eficiencia del Inventario:
       La falta de un análisis sobre los productos menos vendidos o la estacionalidad provoca exceso de stock en ubicaciones equivocadas."""

    ancho_maximo = 87 

    lineas_envueltas = textwrap.wrap(texto_original, width=ancho_maximo)
    texto_formateado = '\n'.join(lineas_envueltas)
    print(texto_formateado)

    
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
        "Enfoque en Rentabilidad y Clientes (Ganancia)": [
            "¿Quiénes son los clientes que generan el 80% de los ingresos?",
            "¿Cuál es el promedio, mínimo y máximo de compra de nuestros clientes y qué tan frecuentes son sus pedidos?",
            "¿Cuál es el cliente que más compra?",
            "¿Cuál es el comportamiento de compra de los clientes en diferentes períodos después de registrarse (30 días, 90 días, etc.)?",
            "¿Cuál es la media de productos por compra y el importe total promedio?"
        ],
        "Enfoque en Inventario y Producto": [
            "¿¿Cuál es la categoría de productos que genera la mayor cantidad de ventas e ingresos?",
            "¿Cuáles son los 10 productos menos vendidos que podrían ser retirados o reemplazados?",
            "¿Cuáles son los productos más frecuentemente consumidos en el primer pedido?"
        ],
        "Enfoque Geográfico y Operativo (Ciudades)": [
            "¿Cómo se distribuyen los ingresos entre las ciudades y cuál genera más rentabilidad?",
            "¿Cuál es el comportamiento de compra de los clientes por períodos después de registrarse?",
            "¿Cuál es el porcentaje de ventas por medio de pago y varía este porcentaje según la ciudad?",
            "¿Cuál es el promedio de ventas por Medio de pago? ¿Cuál es el mes o trimestre con más ingresos?",
            "¿Cuál es el mes o trimestre con más ingresos a nivel general y por ciudad?"
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

def mostrar_solucion():
    """Describe la solución propuesta por el sistema."""
    print("\n---Solución: Un Sistema de Inteligencia de Negocio ---")
    print("El sistema centraliza, calcula y analiza las métricas clave de negocio.")
    print("Su objetivo es transformar los datos de ventas en conocimiento accionable para mejorar la rentabilidad general de la cadena de mini súper y optimizar los esfuerzos en áreas críticas como la atención al cliente, logística e inventario.")
    time.sleep(1)


def cargar_datos():
    """Cargar la tabla maestra limpia para análisis."""
    try:
        # Obtener el directorio del script actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_csv = os.path.join(directorio_actual, 'Tabla_Maestra_limpia.csv')
        
        df = pd.read_csv(ruta_csv)
        print(f"✅ Datos cargados: {len(df)} registros, {len(df.columns)} columnas")
        return df
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'Tabla_Maestra_limpia.csv'")
        print(f"   Buscando en: {ruta_csv if 'ruta_csv' in locals() else 'directorio actual'}")
        return None


def mostrar_estadisticas_descriptivas():
    """REQUISITO 1: Estadísticas descriptivas básicas calculadas."""
    print("\n" + "="*70)
    print("📊 1. ESTADÍSTICAS DESCRIPTIVAS BÁSICAS")
    print("="*70)
    
    df = cargar_datos()
    if df is None:
        return
    
    variables = ['importe', 'cantidad', 'precio_unitario', 'dias_desde_alta']
    
    for var in variables:
        if var in df.columns:
            print(f"\n📈 Variable: {var.upper()}")
            print("-" * 70)
            
            # Medidas de tendencia central
            media = df[var].mean()
            mediana = df[var].median()
            moda = df[var].mode()[0] if len(df[var].mode()) > 0 else 0
            
            # Medidas de dispersión
            desv_std = df[var].std()
            minimo = df[var].min()
            maximo = df[var].max()
            
            # Cuartiles
            q1 = df[var].quantile(0.25)
            q2 = df[var].quantile(0.50)
            q3 = df[var].quantile(0.75)
            
            print(f"  TENDENCIA CENTRAL:")
            print(f"    Media:    {media:,.2f}")
            print(f"    Mediana:  {mediana:,.2f}")
            print(f"    Moda:     {moda:,.2f}")
            
            print(f"\n  DISPERSIÓN:")
            print(f"    Desv. Std: {desv_std:,.2f}")
            print(f"    Mínimo:    {minimo:,.2f}")
            print(f"    Máximo:    {maximo:,.2f}")
            
            print(f"\n  CUARTILES:")
            print(f"    Q1 (25%):  {q1:,.2f}")
            print(f"    Q2 (50%):  {q2:,.2f}")
            print(f"    Q3 (75%):  {q3:,.2f}")
            print(f"    IQR:       {q3 - q1:,.2f}")
            
            time.sleep(0.5)
    
    input("\n✅ Presiona Enter para continuar...")


def mostrar_tipo_distribucion():
    """REQUISITO 2: Identificación del tipo de distribución de variables."""
    print("\n" + "="*70)
    print("📊 2. IDENTIFICACIÓN DEL TIPO DE DISTRIBUCIÓN")
    print("="*70)
    
    df = cargar_datos()
    if df is None:
        return
    
    variables = ['importe', 'cantidad', 'precio_unitario', 'dias_desde_alta']
    
    for var in variables:
        if var in df.columns:
            print(f"\n📈 Variable: {var.upper()}")
            print("-" * 70)
            
            media = df[var].mean()
            mediana = df[var].median()
            skewness = df[var].skew()
            kurtosis = df[var].kurtosis()
            
            # Determinar tipo de distribución
            if abs(media - mediana) / media < 0.05:
                tipo = "NORMAL (Simétrica)"
                interpretacion = "Los datos están distribuidos simétricamente alrededor de la media"
            elif media > mediana:
                tipo = "SESGADA POSITIVA (Cola a la derecha)"
                interpretacion = "Hay valores extremadamente altos que elevan la media"
            else:
                tipo = "SESGADA NEGATIVA (Cola a la izquierda)"
                interpretacion = "Hay valores extremadamente bajos que reducen la media"
            
            print(f"  Media:     {media:,.2f}")
            print(f"  Mediana:   {mediana:,.2f}")
            print(f"  Diferencia: {abs(media - mediana):,.2f} ({abs(media - mediana) / media * 100:.1f}%)")
            print(f"  Asimetría (skewness): {skewness:.2f}")
            print(f"  Curtosis (kurtosis):  {kurtosis:.2f}")
            print(f"\n  🔍 TIPO DE DISTRIBUCIÓN: {tipo}")
            print(f"  💡 INTERPRETACIÓN: {interpretacion}")
            
            time.sleep(0.5)
    
    input("\n✅ Presiona Enter para continuar...")


def mostrar_analisis_correlaciones():
    """REQUISITO 3: Análisis de correlaciones entre variables principales."""
    print("\n" + "="*70)
    print("📊 3. ANÁLISIS DE CORRELACIONES")
    print("="*70)
    
    df = cargar_datos()
    if df is None:
        return
    
    variables_numericas = ['importe', 'cantidad', 'precio_unitario', 'dias_desde_alta']
    vars_disponibles = [v for v in variables_numericas if v in df.columns]
    
    # Calcular matriz de correlación
    correlacion = df[vars_disponibles].corr(method='pearson')
    
    print("\n📊 MATRIZ DE CORRELACIÓN (Pearson)")
    print("-" * 70)
    print(correlacion.round(3))
    
    print("\n💡 INTERPRETACIONES CLAVE:")
    print("-" * 70)
    
    # Encontrar correlaciones significativas
    for i in range(len(vars_disponibles)):
        for j in range(i+1, len(vars_disponibles)):
            var1 = vars_disponibles[i]
            var2 = vars_disponibles[j]
            r = correlacion.loc[var1, var2]
            
            if abs(r) > 0.3:
                if r > 0.7:
                    fuerza = "MUY FUERTE"
                elif r > 0.5:
                    fuerza = "FUERTE"
                else:
                    fuerza = "MODERADA"
                
                direccion = "POSITIVA" if r > 0 else "NEGATIVA"
                
                print(f"\n  {var1} ↔ {var2}:")
                print(f"    Correlación: {r:.3f} ({fuerza} {direccion})")
                
                if r > 0:
                    print(f"    ➡️  Cuando {var1} aumenta, {var2} tiende a aumentar")
                else:
                    print(f"    ➡️  Cuando {var1} aumenta, {var2} tiende a disminuir")
                
                time.sleep(0.3)
    
    print("\n⚠️  IMPORTANTE: Correlación NO implica causalidad")
    
    input("\n✅ Presiona Enter para continuar...")


def mostrar_deteccion_outliers():
    """REQUISITO 4: Detección de outliers (valores extremos)."""
    print("\n" + "="*70)
    print("📊 4. DETECCIÓN DE OUTLIERS (VALORES EXTREMOS)")
    print("="*70)
    
    df = cargar_datos()
    if df is None:
        return
    
    variables = ['importe', 'cantidad', 'precio_unitario', 'dias_desde_alta']
    
    for var in variables:
        if var in df.columns:
            print(f"\n📈 Variable: {var.upper()}")
            print("-" * 70)
            
            q1 = df[var].quantile(0.25)
            q3 = df[var].quantile(0.75)
            iqr = q3 - q1
            
            # Límites para outliers (método IQR)
            limite_inferior = q1 - 1.5 * iqr
            limite_superior = q3 + 1.5 * iqr
            
            # Identificar outliers
            outliers = df[(df[var] < limite_inferior) | (df[var] > limite_superior)]
            
            print(f"  Q1:  {q1:,.2f}")
            print(f"  Q3:  {q3:,.2f}")
            print(f"  IQR: {iqr:,.2f}")
            print(f"  Límite inferior: {limite_inferior:,.2f}")
            print(f"  Límite superior: {limite_superior:,.2f}")
            print(f"\n  🔍 Outliers detectados: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
            
            if len(outliers) > 0:
                valores_unicos = sorted(outliers[var].unique())[:5]
                print(f"  Ejemplos de valores extremos: {valores_unicos}")
                
                if len(outliers) / len(df) > 0.05:
                    print(f"\n  ⚠️  Hay muchos outliers ({len(outliers)/len(df)*100:.1f}%)")
                    print(f"     Analizar si son errores o datos legítimos")
                else:
                    print(f"\n  ✅ Cantidad normal de outliers")
                    print(f"     Pueden representar casos especiales de negocio")
            
            time.sleep(0.5)
    
    input("\n✅ Presiona Enter para continuar...")


def mostrar_graficos():
    """REQUISITO 5: Gráficos representativos disponibles en archivo separado."""
    print("\n" + "="*70)
    print("📊 5. GRÁFICOS REPRESENTATIVOS")
    print("="*70)

    print("\n📈 Los gráficos estadísticos están disponibles en archivos separados:")
    print("\n  📊 Para generar los gráficos, ejecuta:")
    print("     py analisis_estadistico.py")
    
    print("\n  📓 Para explorar gráficos interactivos:")
    print("     Abre Graficos.ipynb en Jupyter Notebook o VS Code")
    
    input("\n✅ Presiona Enter para continuar...")


def mostrar_interpretacion_resultados():
    """REQUISITO 6: Interpretación de resultados orientada al problema."""
    print("\n" + "="*70)
    print("📊 6. INTERPRETACIÓN DE RESULTADOS - ORIENTADA AL NEGOCIO")
    print("="*70)
    
    df = cargar_datos()
    if df is None:
        return
    
    print("\n🎯 HALLAZGOS PRINCIPALES:")
    print("="*70)
    
    # 1. Análisis de ingresos
    print("\n1️⃣  ANÁLISIS DE INGRESOS:")
    print("-" * 70)
    ingreso_promedio = df['importe'].mean()
    ingreso_mediano = df['importe'].median()
    print(f"  • Ticket promedio: ${ingreso_promedio:,.2f}")
    print(f"  • Ticket mediano: ${ingreso_mediano:,.2f}")
    
    if ingreso_promedio > ingreso_mediano * 1.2:
        print(f"  💡 La media es {(ingreso_promedio/ingreso_mediano - 1)*100:.1f}% mayor que la mediana")
        print(f"     Esto indica que hay compras de alto valor que elevan el promedio")
        print(f"     RECOMENDACIÓN: Identificar y fidelizar a clientes de alto ticket")
    else:
        print(f"  ✅ Media y mediana similares: distribución equilibrada de compras")
    
    time.sleep(1)
    
    # 2. Categorías más rentables
    print("\n2️⃣  CATEGORÍAS MÁS RENTABLES:")
    print("-" * 70)
    top_categorias = df.groupby('categoria')['importe'].sum().sort_values(ascending=False).head(3)
    for i, (cat, ing) in enumerate(top_categorias.items(), 1):
        porcentaje = (ing / df['importe'].sum()) * 100
        print(f"  {i}. {cat.title()}: ${ing:,.0f} ({porcentaje:.1f}% del total)")
    
    print(f"\n  💡 RECOMENDACIÓN:")
    print(f"     • Aumentar stock y promociones en '{top_categorias.index[0]}'")
    print(f"     • Analizar por qué estas categorías generan más ingresos")
    
    time.sleep(1)
    
    # 3. Comportamiento temporal
    print("\n3️⃣  COMPORTAMIENTO TEMPORAL:")
    print("-" * 70)
    df['fecha'] = pd.to_datetime(df['fecha'])
    ventas_por_mes = df.groupby(df['fecha'].dt.to_period('M'))['importe'].sum()
    mejor_mes = ventas_por_mes.idxmax()
    peor_mes = ventas_por_mes.idxmin()
    
    print(f"  • Mejor mes: {mejor_mes} (${ventas_por_mes.max():,.0f})")
    print(f"  • Peor mes: {peor_mes} (${ventas_por_mes.min():,.0f})")
    print(f"  • Variación: {(ventas_por_mes.max() / ventas_por_mes.min() - 1)*100:.1f}%")
    
    print(f"\n  💡 RECOMENDACIÓN:")
    print(f"     • Planificar inventario alto para {mejor_mes}")
    print(f"     • Implementar campañas promocionales en meses bajos")
    
    time.sleep(1)
    
    # 4. Resumen ejecutivo
    print("\n" + "="*70)
    print("📋 RESUMEN EJECUTIVO")
    print("="*70)
    print(f"""
  ✅ El negocio tiene un ticket promedio de ${ingreso_promedio:,.2f}
  ✅ La categoría '{top_categorias.index[0]}' genera {(top_categorias.iloc[0] / df['importe'].sum())*100:.1f}% de los ingresos
  ✅ Hay variación significativa en ventas mensuales ({(ventas_por_mes.max() / ventas_por_mes.min() - 1)*100:.1f}%)
  
  🎯 PRIORIDADES ESTRATÉGICAS:
     1. Optimizar inventario en categorías rentables
     2. Implementar programa de fidelización
     3. Planificar campañas para meses de baja venta
     4. Desarrollar segmento B2B para ventas al por mayor
    """)
    
    input("\n✅ Presiona Enter para continuar...")


def ejecutar_analisis_completo():
    """Ejecuta todo el análisis estadístico de forma secuencial."""
    print("\n" + "="*70)
    print("🚀 EJECUTANDO ANÁLISIS ESTADÍSTICO COMPLETO")
    print("="*70)
    
    mostrar_estadisticas_descriptivas()
    mostrar_tipo_distribucion()
    mostrar_analisis_correlaciones()
    mostrar_deteccion_outliers()
    mostrar_graficos()
    mostrar_interpretacion_resultados()
    
    print("\n" + "="*70)
    print("✅ ANÁLISIS ESTADÍSTICO COMPLETADO CON ÉXITO")
    print("="*70)


def mostrar_solucion():
    """Describe la solución propuesta por el sistema."""
    print("\n---Solución: Un Sistema de Inteligencia de Negocio ---")
    print("El sistema centraliza, calcula y analiza las métricas clave de negocio.")
    print("Su objetivo es transformar los datos de ventas en conocimiento accionable para mejorar la rentabilidad general de la cadena de mini súper y optimizar los esfuerzos en áreas críticas como la atención al cliente, logística e inventario.")
    time.sleep(1)


def main():
    """Función principal que orquesta la presentación del proyecto."""
    mostrar_titulo()
    
    opciones = {
        "1": ("Análisis del Problema", mostrar_analisis_problema),
        "2": ("Arquitectura de Datos", mostrar_arquitectura_datos),
        "3": ("Preguntas Estratégicas", mostrar_preguntas_estrategicas),
        "4": ("Stack Tecnológico", mostrar_stack_tecnologico),
        "5": ("Solución Propuesta", mostrar_solucion),
        "6": ("--- ANÁLISIS ESTADÍSTICO ---", None),
        "7": ("Estadísticas Descriptivas", mostrar_estadisticas_descriptivas),
        "8": ("Tipo de Distribución", mostrar_tipo_distribucion),
        "9": ("Análisis de Correlaciones", mostrar_analisis_correlaciones),
        "10": ("Detección de Outliers", mostrar_deteccion_outliers),
        "11": ("Gráficos Representativos", mostrar_graficos),
        "12": ("Interpretación de Resultados", mostrar_interpretacion_resultados),
        "13": ("Ejecutar Análisis Completo", ejecutar_analisis_completo),
        "14": ("Mostrar Todo (Información)", None),
        "15": ("Salir", None)
    }

    while True:
        print("\n" + "="*50)
        print("📋 MENÚ PRINCIPAL - PROYECTO AURELION")
        print("="*50)
        for key, (value, _) in opciones.items():
            print(f"{key}. {value}")
        
        eleccion = input("\nSelecciona una opción: ")

        if eleccion == "15":
            print("\n🎉 ¡Hasta luego! Gracias por usar el sistema.")
            break
        elif eleccion == "14":
            mostrar_analisis_problema()
            mostrar_arquitectura_datos()
            mostrar_preguntas_estrategicas()
            mostrar_stack_tecnologico()
            mostrar_solucion()
            print("\n--- Fin de la presentación completa ---")
        elif eleccion == "6":
            print("\n📊 Las opciones 7-13 contienen el análisis estadístico detallado")
            print("   Selecciona la opción 13 para ejecutar todo el análisis de una vez")
        elif eleccion in opciones:
            _, funcion = opciones[eleccion]
            if funcion:
                funcion()
        else:
            print("❌ Opción no válida. Por favor, intenta de nuevo.")
        
        if eleccion != "15":
            input("\n⏎ Presiona Enter para volver al menú...")


if __name__ == "__main__":
    main()
