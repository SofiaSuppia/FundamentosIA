# 📋 Instrucciones para Ejecutar el Análisis de Ventas

## 🚨 Problema Común: "No such file or directory"

Si te aparece el error:
```
¡ERROR! El programa no encuentra los archivos. Revisa que estén en la misma carpeta que main.py.
```

## ✅ Soluciones:

### **Opción 1: Copiar Archivos (Recomendado)**
1. Asegúrate de tener estos 4 archivos en la **misma carpeta** que `main.py`:
   ```
   📁 Tu Carpeta del Proyecto/
   ├── main.py
   ├── procesoDatos.py
   ├── analisisDatos.py
   ├── Clientes.xlsx          ← NECESARIO
   ├── Productos.xlsx         ← NECESARIO
   ├── Ventas.xlsx            ← NECESARIO
   └── Detalle_ventas.xlsx    ← NECESARIO
   ```

### **Opción 2: Navegar al Directorio Correcto**
1. Abre PowerShell o Terminal
2. Navega a la carpeta donde están los archivos Excel:
   ```powershell
   cd "C:\ruta\a\tu\carpeta\con\archivos"
   ```
3. Ejecuta el programa:
   ```powershell
   python main.py
   ```

## 🔧 Verificación Paso a Paso:

### **1. Verificar que Python esté instalado:**
```powershell
python --version
```
Debería mostrar algo como: `Python 3.x.x`

### **2. Verificar que las librerías estén instaladas:**
```powershell
pip install pandas numpy openpyxl
```

### **3. Verificar que estés en el directorio correcto:**
```powershell
dir
```
Deberías ver todos los archivos .xlsx listados.

### **4. Ejecutar el programa:**
```powershell
python main.py
```

## 📞 Si Sigues Teniendo Problemas:

El programa ahora muestra información de diagnóstico detallada:
- ✅ Archivos encontrados
- ❌ Archivos faltantes
- 📁 Directorio actual
- 💡 Soluciones específicas

**Copia y pega el mensaje completo de error para obtener ayuda específica.**

## 🎯 Resultado Esperado:

Si todo funciona correctamente, deberías ver:
```
--- INICIO DEL ANÁLISIS DE VENTAS ---
📁 Directorio actual: C:\tu\carpeta
📋 Archivos en el directorio:
   ✅ Clientes.xlsx
   ✅ Productos.xlsx
   ✅ Ventas.xlsx
   ✅ Detalle_ventas.xlsx
   ✅ ENCONTRADO: Clientes.xlsx
   ✅ ENCONTRADO: Productos.xlsx
   ✅ ENCONTRADO: Ventas.xlsx
   ✅ ENCONTRADO: Detalle_ventas.xlsx
✅ Todos los archivos están disponibles.
📖 Cargando Clientes.xlsx...
   ✅ Clientes.xlsx cargado exitosamente
...
=======================================================
               RESULTADOS DEL ANÁLISIS
=======================================================
```