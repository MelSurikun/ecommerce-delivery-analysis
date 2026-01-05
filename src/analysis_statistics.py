import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cargar_y_preparar_datos(filepath):
    """
    Carga el dataset limpio y genera las columnas calculadas necesarias para el análisis.
    """
    try:
        df = pd.read_csv(filepath)
        
        # Convertir fechas (crucial para cálculos de tiempo)
        date_cols = ['order_date', 'shipped_date', 'delivered_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # VARIABLE OBJETIVO: Días reales de entrega
        if 'delivered_date' in df.columns and 'shipped_date' in df.columns:
            df['dias_reales'] = (df['delivered_date'] - df['shipped_date']).dt.days
            
        # Extraer mes para análisis temporal
        if 'order_date' in df.columns:
            df['mes_anio'] = df['order_date'].dt.to_period('M')
            
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {filepath}")
        return None

def generar_estadisticas_clave(df):
    """Retorna un resumen estadístico enfocado en tiempos de entrega."""
    resumen = df['dias_reales'].describe().to_frame().T
    resumen['varianza'] = df['dias_reales'].var()
    resumen['skewness'] = df['dias_reales'].skew()  # Sesgo de la distribución
    return resumen

def analizar_factores(df, columna_factor):
    """
    Calcula el tiempo promedio y desviación estándar agrupado por un factor (ej. transportista).
    """
    return df.groupby(columna_factor)['dias_reales'].agg(['mean', 'std', 'count']).sort_values('mean')

# --- FUNCIONES DE VISUALIZACIÓN ---

def plot_distribucion_tiempos(df):
    """Histograma para ver la frecuencia de los días de entrega."""
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='dias_reales', bins=30, kde=True, color='skyblue')
    plt.axvline(df['dias_reales'].mean(), color='red', linestyle='--', label='Promedio')
    plt.title('Distribución de Tiempos de Entrega')
    plt.xlabel('Días')
    plt.legend()
    return plt

def plot_comparativa_boxplots(df, categoria):
    """Boxplot para detectar outliers y comparar varianzas entre grupos."""
    plt.figure(figsize=(12, 6))
    
    # Ordenar por mediana para mejor visualización
    orden = df.groupby(categoria)['dias_reales'].median().sort_values().index
    
    sns.boxplot(data=df, x=categoria, y='dias_reales', order=orden, palette='viridis')
    plt.title(f'Variabilidad de Tiempos por {categoria}')
    plt.xticks(rotation=45)
    return plt

def plot_heatmap_correlaciones(df):
    """Mapa de calor para identificar qué variables afectan el tiempo."""
    plt.figure(figsize=(10, 8))
    # Seleccionamos solo variables numéricas relevantes
    cols = ['dias_reales', 'distance_km', 'shipping_cost_mxn', 'product_price_mxn', 'is_peak_season']
    corr = df[cols].corr()
    
    sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
    plt.title('Matriz de Correlación')
    return plt