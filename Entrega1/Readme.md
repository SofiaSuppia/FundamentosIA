<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto Aurelion - Sistema de Análisis de Ventas</title>
    <style>
        body { font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1, h2, h3, h4 { color: #2c3e50; }
        h1 { border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
        h2 { border-bottom: 1px solid #ccc; padding-bottom: 5px; }
        code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 4px; font-family: monospace; }
        pre { background-color: #f4f4f4; padding: 10px; border-radius: 5px; white-space: pre-wrap; word-wrap: break-word; }
        table { border-collapse: collapse; width: 100%; margin-bottom: 1em; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        blockquote { border-left: 4px solid #ccc; padding-left: 10px; color: #666; margin: 0 0 1em 0; }
    </style>
</head>
<body>

    <h1>🚀 Proyecto Aurelion - Sistema de Análisis de Ventas</h1>
    <blockquote>
        <p><strong>Autor:</strong> Sofia Suppia<br>
        <strong>Fecha:</strong> Octubre 2025<br>
        <strong>Materia:</strong> Fundamentos de Inteligencia Artificial</p>
    </blockquote>
    <hr>

    <h2>🎯 Resumen</h2>
    <h3>Tema Principal</h3>
    <p><strong>Análisis de datos de ventas en un market digital</strong> (modelo JustMart) para identificar patrones de consumo, optimizar decisiones comerciales y diseñar estrategias de fidelización de clientes.</p>

    <h3>Problema Identificado</h3>
    <p>La empresa carece de un sistema automatizado que permita responder preguntas estratégicas clave como:</p>
    <ul>
        <li>🏆 ¿Quiénes son los clientes más valiosos?</li>
        <li>📉 ¿Cuáles son los productos menos vendidos?</li>
        <li>💳 ¿Qué medios de pago son más utilizados?</li>
        <li>🌍 ¿Cuáles son las ciudades más rentables?</li>
    </ul>
    <p>Esta limitación impide la toma de decisiones basadas en datos concretos.</p>

    <h3>Solución Propuesta</h3>
    <p>Desarrollo de un <strong>programa en Python</strong> que integre múltiples fuentes de datos (Ventas, Detalles, Productos y Clientes) utilizando:</p>
    <ul>
        <li>🐼 <strong>Pandas</strong> para procesamiento y análisis de datos</li>
        <li>📊 <strong>Análisis estadístico</strong> para identificar patrones</li>
        <li>🔄 <strong>Integración automatizada</strong> de múltiples tablas relacionales</li>
    </ul>
    <hr>

    <h2>🔍 Análisis del Problema</h2>
    <h3>💼 Contexto Empresarial</h3>
    <p>El proyecto simula el análisis de datos de una tienda digital que necesita optimizar sus operaciones mediante insights basados en datos históricos de ventas.</p>

    <h3>🎯 Objetivos Específicos</h3>
    <ol>
        <li><strong>Identificación de clientes estratégicos</strong> usando análisis Pareto (80/20)</li>
        <li><strong>Optimización del inventario</strong> mediante análisis de productos</li>
        <li><strong>Análisis de rentabilidad geográfica</strong> por ciudades</li>
        <li><strong>Evaluación de métodos de pago</strong> preferidos por los clientes</li>
    </ol>
    <hr>

    <h2>💾 Arquitectura de Datos</h2>
    <h3>📊 Origen de los Datos</h3>
    <p>Los datos provienen de una <strong>simulación de ventas históricas</strong> estructurados en cuatro archivos Excel que representan las tablas principales de un sistema de ventas.</p>

    <h3>🗄️ Estructura de la Base de Datos</h3>
    <h4><strong>Esquema Relacional</strong></h4>
    <pre><code>erDiagram
    CLIENTES ||--o{ VENTAS : "realiza"
    VENTAS ||--o{ DETALLE_VENTAS : "contiene"
    PRODUCTOS ||--o{ DETALLE_VENTAS : "incluye"
    
    CLIENTES {
        int ID_Cliente PK
        string Nombre
        string Ciudad
        date Fecha_Registro
    }
    
    PRODUCTOS {
        int ID_Producto PK
        string Nombre_Producto
        string Categoria
    }
    
    VENTAS {
        int ID_Venta PK
        int ID_Cliente FK
        date Fecha_Venta
        string Medio_Pago
        decimal Monto_Total
    }
    
    DETALLE_VENTAS {
        int ID_Venta FK
        int ID_Producto FK
        int Cantidad
        decimal Precio_Unitario
        decimal Costo_Unitario
        decimal Importe
    }
</code></pre>

    <h4><strong>Especificaciones Técnicas</strong></h4>
    <table>
        <thead>
            <tr>
                <th>📋 <strong>Tabla</strong></th>
                <th>📈 <strong>Registros</strong></th>
                <th>🔗 <strong>Relaciones</strong></th>
                <th>📝 <strong>Campos Principales</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>👥 Clientes</strong></td>
                <td>100</td>
                <td>PK: <code>ID_Cliente</code></td>
                <td>ID, Nombre, Ciudad, Fecha_Registro</td>
            </tr>
            <tr>
                <td><strong>📦 Productos</strong></td>
                <td>100</td>
                <td>PK: <code>ID_Producto</code></td>
                <td>ID, Nombre, Categoría</td>
            </tr>
            <tr>
                <td><strong>🛒 Ventas</strong></td>
                <td>120</td>
                <td>PK: <code>ID_Venta</code> → FK: <code>ID_Cliente</code></td>
                <td>ID_Venta, Fecha, Medio_Pago, Monto</td>
            </tr>
            <tr>
                <td><strong>📋 Detalle_Ventas</strong></td>
                <td>120</td>
                <td>FK: <code>ID_Venta</code>, <code>ID_Producto</code></td>
                <td>Cantidad, Precios, Costos, Importe</td>
            </tr>
        </tbody>
    </table>

    <h3>🔧 Características del Dataset</h3>
    <ul>
        <li><strong>📊 Tipo:</strong> Simulación de Base de Datos Relacional (OLTP → OLAP)</li>
        <li><strong>📏 Escala:</strong> Pequeña a mediana (miles de registros)</li>
        <li><strong>💾 Formato:</strong> Archivos Excel (.xlsx)</li>
        <li><strong>🚀 Procesamiento:</strong> Completamente en memoria con Pandas</li>
    </ul>
    <hr>

    <h2>❓ Preguntas Estratégicas Completas</h2>
    <h3>📊 <strong>Categoría: Análisis de Clientes</strong></h3>
    <h4>🏆 <strong>P1: Clientes con Mayor Rentabilidad</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Quiénes son los clientes que generan un 80% de los ingresos?</li>
        <li><strong>Datos clave:</strong> Clientes + ventas + detalle de ventas</li>
        <li><strong>Metodología:</strong> Análisis Pareto, cálculo de ingresos acumulados y porcentajes</li>
    </ul>
    <h4>💰 <strong>P2: Valor Promedio de minimo y maximo de Compra de nuestros clientes Cliente</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el promedio, mínimo y máximo de compra de nuestros clientes?</li>
        <li><strong>Datos clave:</strong> Ventas + detalle de ventas</li>
        <li><strong>Metodología:</strong> Promedio de monto total por transacción</li>
    </ul>
    <h4>🛒 <strong>P3: Frecuencia de Compra</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Qué tan frecuentes y qué productos compran los clientes más fieles?</li>
        <li><strong>Datos clave:</strong> Detalle de ventas + productos</li>
        <li><strong>Metodología:</strong> Análisis temporal y de productos por cliente</li>
    </ul>
    <h4>📋 <strong>P4: Listado de Top Clientes</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el cliente que más compra?</li>
        <li><strong>Datos clave:</strong> Ventas + detalle de ventas</li>
        <li><strong>Metodología:</strong> Agrupación por cliente, suma de importes, ordenamiento descendente</li>
    </ul>

    <h3>📦 <strong>Categoría: Análisis de Productos</strong></h3>
    <h4>🎯 <strong>P5: Categorías con Mayor Rentabilidad</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es la categoría de productos que tiene la mayor cantidad de productos vendidos? ¿Me podes decir los ingresos de cada categoría?</li>
        <li><strong>Datos clave:</strong> Detalle de ventas + productos</li>
        <li><strong>Metodología:</strong> Agrupación por categoría, suma de cantidades</li>
    </ul>
    <h4>🔍 <strong>P6: Productos Menos Vendidos</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> Hacer lista de los 10 productos menos vendidos</li>
        <li><strong>Datos clave:</strong> Detalle de ventas + productos</li>
        <li><strong>Metodología:</strong> Agrupación por producto, suma de cantidades, ordenamiento ascendente</li>
    </ul>
    <h4>💎 <strong>P7: Productos Más Frecuentes en Primeras Compras</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuáles son los productos más frecuentemente consumidos en el primer pedido?</li>
        <li><strong>Datos clave:</strong> Detalle de ventas</li>
        <li><strong>Metodología:</strong> Identificación de primeras compras, análisis de frecuencia</li>
    </ul>

    <h3>🏙️ <strong>Categoría: Análisis Geográfico</strong></h3>
    <h4>🌍 <strong>P8: Distribución Geográfica de Ingresos</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cómo se distribuyen los ingresos entre las ciudades? ¿Hay alguna ciudad que genere más ingresos?</li>
        <li><strong>Datos clave:</strong> Ventas + clientes</li>
        <li><strong>Metodología:</strong> Join de tablas, agrupación por ciudad</li>
    </ul>
    <h4>📍 <strong>P9: Volumen de Ventas por Ciudad</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el volumen de ventas promedio de los clientes en los primeros 30 días para cada ciudad?</li>
        <li><strong>Datos clave:</strong> Clientes, ventas, detalle de ventas</li>
        <li><strong>Metodología:</strong> Análisis temporal por ciudad, filtros de fecha</li>
    </ul>

    <h3>💳 <strong>Categoría: Análisis de Medios de Pago</strong></h3>
    <h4>📊 <strong>P10: Análisis de Medios de Pago</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el porcentaje de ventas por medio de pago y varía este porcentaje según la ciudad?</li>
        <li><strong>Datos clave:</strong> Ventas</li>
        <li><strong>Metodología:</strong> Cálculo de porcentajes, análisis por ciudad</li>
    </ul>
    <h4>💰 <strong>P11: Monto Promedio por Medio de Pago</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> Identificar los medios de pago que usan los clientes para evitar...</li>
        <li><strong>Datos clave:</strong> Ventas</li>
        <li><strong>Metodología:</strong> Análisis de frecuencia de medios de pago</li>
    </ul>

    <h3>📈 <strong>Categoría: Análisis Temporal y Tendencias</strong></h3>
    <h4>📅 <strong>P12: Estacionalidad de Ventas</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el mes o trimestre con más ingresos?</li>
        <li><strong>Datos clave:</strong> Ventas (cálculos con fecha)</li>
        <li><strong>Metodología:</strong> Agrupación temporal, suma de montos</li>
    </ul>
    <h4>⏱️ <strong>P13: Análisis de Comportamiento de Activación de Clientes</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el comportamiento de compra de los clientes en diferentes períodos después de registrarse en la plataforma? (30 días, 90 días, 6 meses, 1 año)</li>
        <li><strong>Datos clave:</strong> Ventas + clientes + análisis temporal multiperíodo</li>
        <li><strong>Metodología:</strong> Cálculo de diferencias temporales <code>(fecha_venta - fecha_registro).dt.days</code>, filtros por múltiples períodos, análisis de activación progresiva</li>
    </ul>

    <h3>💲 <strong>Categoría: Análisis de Precios y Costos</strong></h3>
    <h4>🏷️ <strong>P14: Análisis de Precios por Categoría</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el precio unitario promedio de los productos por categoría?</li>
        <li><strong>Datos clave:</strong> Detalle de ventas + productos</li>
        <li><strong>Metodología:</strong> Agrupación por categoría, promedio de precios</li>
    </ul>
    <h4>📈 <strong>P15: Rentabilidad por Producto</strong></h4>
    <ul>
        <li><strong>Enunciado:</strong> ¿Cuál es el monto de compra promedio comparado con el precio unitario promedio (diferenciadas valor y volumen)?</li>
        <li><strong>Datos clave:</strong> Detalle de ventas + productos</li>
        <li><strong>Metodología:</strong> Análisis de márgenes y rentabilidad</li>
    </ul>
    <hr>

    <h2>💰 Metodología: Cálculo de Costo Unitario y Ganancia Bruta</h2>
    <h3>🎯 <strong>Objetivo</strong></h3>
    <p>Calcular el costo unitario y la ganancia bruta para cada producto en las ventas, utilizando numpy para análisis eficiente y identificar los productos menos rentables.</p>

    <h3>📐 <strong>Fórmulas de Cálculo</strong></h3>
    <h4><strong>Cálculo de Costo Unitario</strong></h4>
    <pre><code># Fórmula principal con margen de ganancia bruta del 30%
Costo_Unitario = Precio_Unitario / 1.30

# Equivalente: Si el margen es 30%, el costo representa el 76.92% del precio
Costo_Unitario = Precio_Unitario * 0.7692
</code></pre>

    <h4><strong>Cálculo de Ganancia Bruta</strong></h4>
    <pre><code># Fórmula de Ganancia Bruta
Ganancia_Bruta = Importe - (Costo_Unitario × Cantidad)

# Donde:
# - Importe = Ingresos totales de la venta del producto
# - Costo_Unitario = Costo calculado usando la fórmula anterior
# - Cantidad = Unidades vendidas del producto
</code></pre>

    <h3>🎯 <strong>Justificación de la Metodología</strong></h3>
    <h4><strong>¿Por qué <code>Costo_Unitario = Precio_Unitario / 1.30</code>?</strong></h4>
    <table>
        <thead>
            <tr>
                <th>🧮 <strong>Concepto</strong></th>
                <th><strong>Valor</strong></th>
                <th>📋 <strong>Explicación</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Margen de Ganancia Bruta</strong></td>
                <td>30%</td>
                <td>Porcentaje de ganancia deseado sobre el precio de venta</td>
            </tr>
            <tr>
                <td><strong>Factor de Cálculo</strong></td>
                <td>1.30</td>
                <td>Si el costo + 30% = precio, entonces precio / 1.30 = costo</td>
            </tr>
            <tr>
                <td><strong>Porcentaje del Costo</strong></td>
                <td>76.92%</td>
                <td>El costo representa el 76.92% del precio de venta</td>
            </tr>
            <tr>
                <td><strong>Margen Bruto Real</strong></td>
                <td>23.08%</td>
                <td>Porcentaje real del margen sobre el precio total</td>
            </tr>
        </tbody>
    </table>

    <h4><strong>Ejemplo Práctico:</strong></h4>
    <pre><code># Si un producto se vende a $100
precio_unitario = 100.00

# Costo unitario con margen del 30%
costo_unitario = precio_unitario / 1.30  # = $76.92

# Ganancia por unidad
ganancia_por_unidad = precio_unitario - costo_unitario  # = $23.08

# Margen bruto porcentual
margen_bruto = (ganancia_por_unidad / precio_unitario) * 100  # = 23.08%
</code></pre>
    <hr>

    <h2>⚙️ Planificación del Desarrollo</h2>
    <h3>📁 Archivos de Entrada Requeridos</h3>
    <p>El sistema necesita los siguientes archivos para su correcto funcionamiento:</p>
    <table>
        <thead>
            <tr>
                <th>📄 <strong>Archivo</strong></th>
                <th>🔧 <strong>Campos Requeridos</strong></th>
                <th>📋 <strong>Descripción</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><code>Clientes.xlsx</code></td>
                <td>ID_Cliente, Nombre, Ciudad, Fecha_Registro</td>
                <td>Base de datos de clientes registrados</td>
            </tr>
            <tr>
                <td><code>Productos.xlsx</code></td>
                <td>ID_Producto, Nombre_Producto, Categoría</td>
                <td>Catálogo completo de productos</td>
            </tr>
            <tr>
                <td><code>Ventas.xlsx</code></td>
                <td>ID_Venta, ID_Cliente, Fecha_Venta, Medio_Pago, Monto_Total</td>
                <td>Registro de transacciones</td>
            </tr>
            <tr>
                <td><code>Detalle_ventas.xlsx</code></td>
                <td>ID_Venta, ID_Producto, Cantidad, Precio_Unitario, Costo_Unitario</td>
                <td>Detalle línea por línea de cada venta</td>
            </tr>
        </tbody>
    </table>

    <h3>🔄 Flujo de Procesamiento</h3>
    <ol>
        <li><strong>📥 Carga y Preparación</strong>
            <ul>
                <li>Lectura de archivos Excel con Pandas</li>
                <li>Validación de integridad de datos</li>
                <li>Conversión de tipos de datos (fechas, números)</li>
                <li>Simulación de <code>costo_unitario</code> (margen del 30%)</li>
            </ul>
        </li>
        <li><strong>🔗 Integración de Datos</strong>
            <ul>
                <li>Joins entre tablas relacionales</li>
                <li>Creación del DataFrame maestro</li>
                <li>Validación de integridad referencial</li>
            </ul>
        </li>
        <li><strong>📊 Análisis y Resultados</strong>
            <ul>
                <li>Implementación de análisis Pareto</li>
                <li>Cálculos estadísticos por categoría</li>
                <li>Generación de reportes automáticos</li>
            </ul>
        </li>
    </ol>
    <hr>

    <h2>🔧 Implementación Técnica</h2>
    <h3>🐍 Stack Tecnológico</h3>
    <table>
        <thead>
            <tr>
                <th>🛠️ <strong>Herramienta</strong></th>
                <th>📝 <strong>Propósito</strong></th>
                <th>📋 <strong>Funcionalidades</strong></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Python 3.8+</strong></td>
                <td>Lenguaje principal</td>
                <td>Procesamiento y lógica de negocio</td>
            </tr>
            <tr>
                <td><strong>Pandas</strong></td>
                <td>Manipulación de datos</td>
                <td>DataFrames, joins, agrupaciones</td>
            </tr>
            <tr>
                <td><strong>NumPy</strong></td>
                <td>Cálculos numéricos</td>
                <td>Operaciones matemáticas eficientes</td>
            </tr>
            <tr>
                <td><strong>Openpyxl</strong></td>
                <td>Lectura de Excel</td>
                <td>Importación de archivos .xlsx</td>
            </tr>
        </tbody>
    </table>

</body>
</html>
