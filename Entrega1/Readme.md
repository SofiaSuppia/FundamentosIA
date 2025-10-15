<h1 align="center">
    <b>Hola, somos Proyecto Aurelion</b>
    <img src="https://media.giphy.com/media/hvRJCLFzcasrR4ia7z/giphy.gif" width="40">
</h1>

<div align="center">
    Un sistema inteligente de análisis de ventas.
</div>

<br>

<div style="display: flex; justify-content: center; gap: 200px; margin-top: 30px;">
    <a href="https://www.python.org" target="_blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge">
    </a>

   <a href="https://pandas.pydata.org/" target="_blank">
        <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas Badge">
    </a>

  <a href="https://numpy.org/" target="_blank">
      <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy Badge">
  </a>

  <a href="https://openpyxl.readthedocs.io/en/stable/" target="_blank">
      <img src="https://img.shields.io/badge/Openpyxl-107C41?style=for-the-badge&logo=python&logoColor=white" alt="Openpyxl Badge">
  </a>
</div>

<hr>

<h2>🔍 Análisis del Problema Estratégico y la Solución</h2>

<h3>El Desafío: Visión de Rentabilidad Descentralizada</h3>
<p>
    El <strong>Proyecto Aurelion</strong> aborda el desafío central que enfrentan las cadenas de mini súper con presencia en <strong>múltiples ciudades</strong>: la <strong>falta de una visión unificada y analítica de la rentabilidad</strong> que permita optimizar la operación y la experiencia del cliente en cada ubicación. Actualmente, la empresa genera un gran volumen de datos de ventas, pero carece de un sistema automatizado para convertir estos datos en <strong>información estratégica y accionable</strong>. Esta <strong>ceguera analítica</strong> impide:
</p>
<ol>
    <li><strong>Optimizar la Rentabilidad Geográfica:</strong> No se sabe con certeza qué ciudades, clientes o categorías de productos están impulsando realmente las ganancias.</li>
    <li><strong>Personalizar la Atención y Fidelización:</strong> Es imposible identificar y recompensar a los <strong>clientes más valiosos</strong>, ni entender su comportamiento de compra a lo largo del tiempo.</li>
    <li><strong>Mejorar la Eficiencia del Inventario:</strong> La falta de un análisis sobre los productos menos vendidos o la estacionalidad provoca exceso de <em>stock</em> en ubicaciones equivocadas.</li>
</ol>

<h3>Solución: Un Sistema de Inteligencia de Negocio</h3>
<p>
    El sistema centraliza, calcula y analiza las métricas clave de negocio. Su objetivo es transformar los datos de ventas en conocimiento accionable para mejorar la rentabilidad general de la cadena de mini súper y optimizar los esfuerzos en áreas críticas como la atención al cliente, logística e inventario.
</p>

<hr>

<h2>&#x2753; Preguntas Críticas Resueltas por el Sistema</h2>
<p><strong>📊 Enfoque en Rentabilidad y Clientes (Ganancia)</strong><br>
  <ol>
    <li><strong>Análisis Pareto (P1):</strong> ¿Quiénes son los clientes que generan el 80% de los ingresos?<br></li>
    <li><strong>Comportamiento de Compra (P2, P3):</strong> ¿Cuál es el promedio, mínimo y máximo de compra de nuestros clientes y qué tan frecuentes son sus pedidos?<br></li>
    <li><strong>Activación y Lealtad (P13):</strong> ¿Cuál es el comportamiento de compra de los clientes en diferentes períodos después de registrarse (30 días, 90 días, etc.)?</li>
  </ol>
</p>

<p><strong>📦 Enfoque en Inventario y Producto</strong><br>
   <ol>
    <li><strong>Ingreso por Categoría (P5):</strong> ¿Cuál es la categoría de productos que genera la mayor cantidad de ventas e ingresos?<br></li>
    <li><strong>Optimización de Stock (P6):</strong> ¿Cuáles son los <strong>10 productos menos vendidos</strong> que podrían ser retirados o reemplazados?<br></li>
    <li><strong>Fidelización Inicial (P7):</strong> ¿Cuáles son los productos más frecuentemente consumidos en el <strong>primer pedido</strong>?</li>
  </ol>
</p>

<p><strong>🌍 Enfoque Geográfico y Operativo (Ciudades)</strong><br>
   <ol>
    <li><strong>Rendimiento Regional (P8):</strong> ¿Cómo se distribuyen los ingresos entre las ciudades y cuál genera más rentabilidad?<br></li>
    <li><strong>Medio de Pago por Ciudad (P10, P11):</strong> ¿Varía el porcentaje de ventas por medio de pago según la ciudad?<br></li>
    <li><strong>Tendencia Temporal (P12):</strong> ¿Cuál es el mes o trimestre con más ingresos a nivel general y por ciudad?</li>
  </ol>
</p>

<hr>

<h2>&#x1F5C3; Estructura y Composición de la Base de Datos</h2>
<p>El sistema de análisis de ventas se basa en un conjunto de <strong>cuatro tablas relacionales</strong> que capturan la información de transacciones y entidades de negocio. El diseño original es un esquema transaccional, lo que requiere un proceso de <strong>ETL (Extracción, Transformación y Carga)</strong> para unificar la información y responder a las preguntas estratégicas.</p>

<hr>

<h3>1. Composición y Estructura Detallada de las Tablas</h3>
<table border="1" width="100%">
    <thead>
        <tr>
            <th>Tabla (Archivo)</th>
            <th>Clave Primaria (PK)</th>
            <th>Claves Foráneas (FK)</th>
            <th>Columnas Clave y Tipo de Dato</th>
            <th>Registros (Estimado)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Clientes</strong></td>
            <td><code>id_cliente</code></td>
            <td>N/A</td>
            <td><code>nombre_cliente</code>, <code>ciudad</code>, <code>fecha_alta</code></td>
            <td>~100</td>
        </tr>
        <tr>
            <td><strong>Productos</strong></td>
            <td><code>id_producto</code></td>
            <td>N/A</td>
            <td><code>nombre_producto</code>, <code>categoria</code>, <code>precio_unitario</code></td>
            <td>~100</td>
        </tr>
        <tr>
            <td><strong>Ventas</strong></td>
            <td><code>id_venta</code></td>
            <td><code>id_cliente</code></td>
            <td><code>fecha</code>, <code>medio_pago</code></td>
            <td>~112</td>
        </tr>
        <tr>
            <td><strong>Detalle_ventas</strong></td>
            <td>N/A (Compuesta)</td>
            <td><code>id_venta</code>, <code>id_producto</code></td>
            <td><code>cantidad</code>, <code>precio_unitario</code>, <code>importe</code></td>
            <td>~500+</td>
        </tr>
    </tbody>
</table>

<hr>
<h3>2. Explicación del Esquema Relacional (Joins)</h3>
<p>El modelo utiliza claves para conectar lógicamente las transacciones con sus atributos. La tabla <strong><code>Detalle_ventas</code></strong> es el corazón del análisis y se conecta a las demás dimensiones:</p>
<ul>
    <li>&#x1F449; <strong>Venta a Cliente:</strong> <code>Ventas.id_cliente</code> enlaza con <code>Clientes.id_cliente</code>.</li>
    <li>&#x1F449; <strong>Detalle a Producto:</strong> <code>Detalle_ventas.id_producto</code> enlaza con <code>Productos.id_producto</code>.</li>
    <li>&#x1F449; <strong>Detalle a Venta:</strong> <code>Detalle_ventas.id_venta</code> enlaza con <code>Ventas.id_venta</code>.</li>
</ul>
<hr>
<h3>3. &#x1F6A7; Reflexiones sobre la Base de Datos y Desafíos</h3>
<h4>A. Desafíos (Justificación del ETL)</h4>
<p>La estructura transaccional requiere la <strong>Transformación de Datos</strong> (ETL) debido a:</p>
<ul>
    <li><strong>Rentabilidad Inexistente:</strong> La métrica de <strong><code>Ganancia Bruta</code></strong> debe ser <strong>calculada</strong> y no existe en los archivos de origen.</li>
    <li><strong>Venta Fragmentada:</strong> El <strong><code>Monto Total de la Venta</code></strong> debe ser calculado sumando ítems de la tabla <code>Detalle_ventas</code>.</li>
    <li><strong>Integración:</strong> Es necesaria la <strong>unión total</strong> de las 4 tablas en un <strong>DataFrame Maestro</strong> para el análisis eficiente.</li>
</ul>

<h4>B. Redundancias Observadas</h4>
<p>Se identifican campos redundantes comunes en sistemas transaccionales que son gestionados en el ETL:</p>
<ul>
    <li>La tabla <code>Ventas</code> repite atributos de cliente (`nombre_cliente`, `email`).</li>
    <li>La tabla <code>Detalle_ventas</code> repite atributos de producto (`nombre_producto`, `precio_unitario`).</li>
</ul>
