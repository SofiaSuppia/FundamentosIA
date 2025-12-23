import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, r2_score, mean_squared_error
import os

# Configuración de estilo para gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def cargar_y_generar_ventas(n_ventas=3000):
    """
    Carga los productos y clientes limpios, y genera una tabla de ventas 
    sintética actualizada para asegurar que todos los nuevos productos tengan datos.
    """
    print("🔄 Generando datos de ventas actualizados para el modelo...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cargar datos base
    df_clientes = pd.read_csv(os.path.join(script_dir, 'Clientes_limpio.csv'))
    df_productos = pd.read_csv(os.path.join(script_dir, 'Productos_limpio.csv'))
    
    nuevas_ventas = []
    nuevos_detalles = []
    
    fechas = pd.date_range(start='2024-01-01', end='2024-12-31').astype(str)
    medios_pago = ['Efectivo', 'Tarjeta Debito', 'Tarjeta Credito', 'Transferencia', 'Billetera Virtual']
    
    for i in range(n_ventas):
        id_venta = i + 1
        
        # Selección aleatoria
        cliente = df_clientes.sample(1).iloc[0]
        producto = df_productos.sample(1).iloc[0]
        fecha_str = np.random.choice(fechas)
        fecha_dt = pd.to_datetime(fecha_str)
        
        cantidad = np.random.randint(1, 5)
        precio = producto['precio_unitario']
        importe = cantidad * precio
        
        # Registro Venta
        nuevas_ventas.append({
            'id_venta': id_venta,
            'id_cliente': cliente['id_cliente'],
            'fecha': fecha_str,
            'medio_pago': np.random.choice(medios_pago),
            'monto_total': importe, # Simplificación: 1 venta = 1 producto para este dataset ML
            'mes': fecha_dt.month,
            'trimestre': fecha_dt.quarter
        })
        
        # Registro Detalle
        nuevos_detalles.append({
            'id_venta': id_venta,
            'id_producto': producto['id_producto'],
            'cantidad': cantidad,
            'precio_unitario': precio,
            'importe': importe
        })
        
    df_ventas = pd.DataFrame(nuevas_ventas)
    df_detalle = pd.DataFrame(nuevos_detalles)
    
    # Guardar para referencia
    df_ventas.to_csv(os.path.join(script_dir, 'Ventas_limpio.csv'), index=False)
    df_detalle.to_csv(os.path.join(script_dir, 'Detalle_ventas_limpio.csv'), index=False)
    
    return df_ventas, df_detalle, df_clientes, df_productos

def preparar_dataset_maestro(df_v, df_d, df_c, df_p):
    """Une todas las tablas en un solo dataset para ML"""
    m1 = pd.merge(df_d, df_p[['id_producto', 'categoria', 'nombre_producto']], on='id_producto')
    m2 = pd.merge(m1, df_v[['id_venta', 'id_cliente', 'medio_pago', 'fecha', 'mes', 'trimestre']], on='id_venta')
    maestro = pd.merge(m2, df_c[['id_cliente', 'ciudad']], on='id_cliente')
    return maestro

def entrenar_modelos():
    # 1. Obtener datos
    df_v, df_d, df_c, df_p = cargar_y_generar_ventas()
    df = preparar_dataset_maestro(df_v, df_d, df_c, df_p)
    
    print(f"\n📊 Dataset Maestro creado con {len(df)} registros.")
    
    # 2. Preprocesamiento (Label Encoding)
    le_ciudad = LabelEncoder()
    le_pago = LabelEncoder()
    le_cat = LabelEncoder()
    
    df['ciudad_n'] = le_ciudad.fit_transform(df['ciudad'])
    df['pago_n'] = le_pago.fit_transform(df['medio_pago'])
    df['categoria_n'] = le_cat.fit_transform(df['categoria'])
    
    # ==========================================
    # MODELO 1: CLASIFICACIÓN (Random Forest)
    # Objetivo: Predecir la CATEGORÍA del producto
    # ==========================================
    print("\n🤖 Entrenando Modelo 1: Clasificación (Predicción de Categoría)...")
    
    X_cls = df[['ciudad_n', 'pago_n', 'mes', 'trimestre', 'cantidad', 'importe']]
    y_cls = df['categoria_n']
    
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_cls, y_cls, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_c, y_train_c)
    y_pred_c = clf.predict(X_test_c)
    
    acc = accuracy_score(y_test_c, y_pred_c)
    print(f"   ✅ Precisión del Clasificador: {acc:.2%}")
    print("\nReporte de Clasificación:")
    print(classification_report(y_test_c, y_pred_c, target_names=le_cat.classes_))
    
    # Gráfico 1: Matriz de Confusión
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test_c, y_pred_c)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=le_cat.classes_, yticklabels=le_cat.classes_)
    plt.title('Matriz de Confusión - Clasificación de Categorías')
    plt.ylabel('Real')
    plt.xlabel('Predicho')
    plt.tight_layout()
    plt.savefig('grafico_confusion_matrix.png')
    print("   📈 Gráfico guardado: grafico_confusion_matrix.png")

    # Gráfico 2: Importancia de Variables (Clasificación)
    plt.figure(figsize=(10, 5))
    importances_c = pd.Series(clf.feature_importances_, index=X_cls.columns).sort_values(ascending=False)
    sns.barplot(x=importances_c.values, y=importances_c.index, palette='viridis')
    plt.title('Importancia de Variables (Modelo Clasificación)')
    plt.tight_layout()
    plt.savefig('grafico_feature_importance_cls.png')
    print("   📈 Gráfico guardado: grafico_feature_importance_cls.png")

    # ==========================================
    # MODELO 2: REGRESIÓN (Random Forest)
    # Objetivo: Predecir el IMPORTE de la venta
    # ==========================================
    print("\n🤖 Entrenando Modelo 2: Regresión (Predicción de Importe de Venta)...")
    
    # Para regresión usamos la categoría como input también
    X_reg = df[['ciudad_n', 'pago_n', 'mes', 'categoria_n', 'cantidad']]
    y_reg = df['importe']
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    reg = RandomForestRegressor(n_estimators=100, random_state=42)
    reg.fit(X_train_r, y_train_r)
    y_pred_r = reg.predict(X_test_r)
    
    r2 = r2_score(y_test_r, y_pred_r)
    rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))
    print(f"   ✅ R2 Score (Explicación de varianza): {r2:.2f}")
    print(f"   ✅ RMSE (Error cuadrático medio): ${rmse:.2f}")
    
    # Gráfico 3: Predicción vs Realidad
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test_r, y_pred_r, alpha=0.5, color='purple')
    plt.plot([y_test_r.min(), y_test_r.max()], [y_test_r.min(), y_test_r.max()], 'k--', lw=2)
    plt.xlabel('Importe Real')
    plt.ylabel('Importe Predicho')
    plt.title('Regresión: Importe Real vs Predicho')
    plt.tight_layout()
    plt.savefig('grafico_regresion_pred_vs_real.png')
    print("   📈 Gráfico guardado: grafico_regresion_pred_vs_real.png")

    # Gráfico 4: Distribución de Ventas por Categoría
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='categoria', y='importe', data=df, palette='Set2')
    plt.title('Distribución de Importes por Categoría')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('grafico_distribucion_importes.png')
    print("   📈 Gráfico guardado: grafico_distribucion_importes.png")

if __name__ == "__main__":
    entrenar_modelos()
