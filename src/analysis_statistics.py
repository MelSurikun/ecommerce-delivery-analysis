# src/analysis_statistics.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def cargar_y_preparar_datos(filepath):
    """Carga y prepara el dataset calculando días reales y fechas."""
    try:
        df = pd.read_csv(filepath)
        date_cols = ['order_date', 'shipped_date', 'delivered_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Variable Objetivo
        if 'delivered_date' in df.columns and 'shipped_date' in df.columns:
            df['dias_reales'] = (df['delivered_date'] - df['shipped_date']).dt.days
            
        # Extraer mes
        if 'order_date' in df.columns:
            df['mes_anio'] = df['order_date'].dt.to_period('M')
            
        return df
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado en {filepath}")
        return None

def generar_estadisticas_clave(df):
    """Resumen estadístico general."""
    resumen = df['dias_reales'].describe().to_frame().T
    resumen['varianza'] = df['dias_reales'].var()
    resumen['skewness'] = df['dias_reales'].skew()
    return resumen

def prueba_estadistica(df, col_categoria):
    """
    Realiza una prueba estadística (ANOVA) para ver si las diferencias son significativas.
    Retorna: (F-statistic, p-value, Interpretación)
    """
    grupos = [grupo['dias_reales'].dropna() for name, grupo in df.groupby(col_categoria)]
    
    if len(grupos) < 2:
        return "N/A", "N/A", "Menos de 2 grupos"
    
    f_val, p_val = stats.f_oneway(*grupos)
    significancia = "SI" if p_val < 0.05 else "NO"
    
    return f_val, p_val, significancia

def analizar_impacto_categoria(df, col_categoria, titulo_grafico=None):
    """
    Función Maestra: Genera tabla de métricas + Prueba estadística + Boxplot.
    """
    print(f"\n>>> ANÁLISIS DE: {col_categoria.upper()} <<<")
    
    # 1. Tabla de Métricas
    metricas = df.groupby(col_categoria)['dias_reales'].agg(
        Promedio='mean', 
        Mediana='median', 
        Desv_Std='std', 
        Total_Envios='count'
    ).sort_values('Promedio')
    
    # 2. Prueba Estadística
    f, p, es_sig = prueba_estadistica(df, col_categoria)
    print(f"¿Diferencia significativa (p<0.05)? {es_sig} (p-value={p:.4f})")
    
    # 3. Visualización
    plt.figure(figsize=(12, 6))
    orden = metricas.index
    sns.boxplot(data=df, x=col_categoria, y='dias_reales', order=orden, palette='viridis')
    plt.title(titulo_grafico if titulo_grafico else f'Impacto de {col_categoria} en Tiempos de Entrega')
    plt.ylabel('Días Reales')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y', alpha=0.3)
    
    return metricas, plt

def plot_heatmap_correlaciones(df):
    """Mapa de calor de variables numéricas."""
    plt.figure(figsize=(10, 8))
    cols = ['dias_reales', 'distance_km', 'shipping_cost_mxn', 'product_price_mxn', 'is_peak_season']
    # Filtrar solo columnas que existen
    cols = [c for c in cols if c in df.columns]
    corr = df[cols].corr()
    sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
    plt.title('Matriz de Correlación')
    return plt