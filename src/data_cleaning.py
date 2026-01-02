"""
Módulo de limpieza de datos para el proyecto ecommerce-delivery-analysis
Persona 2: Ingeniero de Calidad y Limpieza de Datos
"""

import pandas as pd
import numpy as np


def detectar_valores_faltantes(df):
    """
    Detecta valores faltantes en el DataFrame.
    """
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    
    missing_df = pd.DataFrame({
        'Columna': missing.index,
        'Valores_Faltantes': missing.values,
        'Porcentaje': missing_pct.values
    })
    
    return missing_df[missing_df['Valores_Faltantes'] > 0].sort_values('Valores_Faltantes', ascending=False)


def limpiar_valores_faltantes(df):
    """
    Limpia valores faltantes del DataFrame usando mediana para variables numéricas.
    """
    df_clean = df.copy()
    
    columnas_numericas = ['product_price_mxn', 'shipping_cost_mxn', 'distance_km', 'customer_loyalty_months']
    
    for col in columnas_numericas:
        if col in df_clean.columns:
            df_clean[col].fillna(df_clean[col].median(), inplace=True)
    
    return df_clean


def detectar_duplicados(df):
    """
    Detecta registros duplicados por order_id.
    """
    duplicados = df[df['order_id'].duplicated(keep=False)]
    return duplicados


def limpiar_duplicados(df):
    """
    Elimina registros duplicados manteniendo el primero.
    """
    df_clean = df.copy()
    df_clean = df_clean.drop_duplicates(subset=['order_id'], keep='first')
    
    return df_clean


def detectar_fechas_inconsistentes(df):
    """
    Detecta fechas con lógica inconsistente.
    """
    df_temp = df.copy()
    
    df_temp['order_date'] = pd.to_datetime(df_temp['order_date'])
    df_temp['shipped_date'] = pd.to_datetime(df_temp['shipped_date'])
    df_temp['delivered_date'] = pd.to_datetime(df_temp['delivered_date'])
    
    fechas_invalidas = df_temp[
        (df_temp['shipped_date'] < df_temp['order_date']) |
        (df_temp['delivered_date'] < df_temp['shipped_date'])
    ]
    
    return fechas_invalidas


def limpiar_fechas_inconsistentes(df):
    """
    Elimina registros con fechas inconsistentes.
    """
    df_clean = df.copy()
    
    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])
    df_clean['shipped_date'] = pd.to_datetime(df_clean['shipped_date'])
    df_clean['delivered_date'] = pd.to_datetime(df_clean['delivered_date'])
    
    df_clean = df_clean[
        (df_clean['shipped_date'] >= df_clean['order_date']) &
        (df_clean['delivered_date'] >= df_clean['shipped_date'])
    ]
    
    return df_clean


def detectar_outliers_precio(df):
    """
    Detecta outliers en precios usando método IQR.
    """
    Q1 = df['product_price_mxn'].quantile(0.25)
    Q3 = df['product_price_mxn'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[
        (df['product_price_mxn'] < lower_bound) | 
        (df['product_price_mxn'] > upper_bound)
    ]
    
    return outliers


def detectar_outliers_distancia(df):
    """
    Detecta outliers en distancias usando método IQR.
    """
    Q1 = df['distance_km'].quantile(0.25)
    Q3 = df['distance_km'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[
        (df['distance_km'] < lower_bound) | 
        (df['distance_km'] > upper_bound)
    ]
    
    return outliers


def limpiar_outliers(df):
    """
    Elimina registros con outliers extremos en precio y distancia.
    """
    df_clean = df.copy()
    
    Q1_precio = df_clean['product_price_mxn'].quantile(0.25)
    Q3_precio = df_clean['product_price_mxn'].quantile(0.75)
    IQR_precio = Q3_precio - Q1_precio
    upper_precio = Q3_precio + 3 * IQR_precio
    
    Q1_dist = df_clean['distance_km'].quantile(0.25)
    Q3_dist = df_clean['distance_km'].quantile(0.75)
    IQR_dist = Q3_dist - Q1_dist
    upper_dist = Q3_dist + 3 * IQR_dist
    
    df_clean = df_clean[
        (df_clean['product_price_mxn'] <= upper_precio) &
        (df_clean['distance_km'] <= upper_dist)
    ]
    
    return df_clean


def detectar_typos_transportistas(df):
    """
    Detecta errores tipográficos en nombres de transportistas.
    """
    typos = []
    for carrier in df['shipping_carrier'].unique():
        if carrier != carrier.strip() or '  ' in carrier:
            typos.append(carrier)
    
    return typos


def limpiar_typos_transportistas(df):
    """
    Corrige typos en nombres de transportistas eliminando espacios extras.
    """
    df_clean = df.copy()
    df_clean['shipping_carrier'] = df_clean['shipping_carrier'].str.strip()
    
    return df_clean


def limpiar_dataset_completo(df):
    """
    Aplica todas las funciones de limpieza al dataset.
    """
    print("Iniciando proceso de limpieza...")
    print(f"Registros iniciales: {len(df)}")
    
    df_clean = limpiar_typos_transportistas(df)
    print("1. Typos corregidos")
    
    df_clean = limpiar_valores_faltantes(df_clean)
    print("2. Valores faltantes imputados")
    
    registros_antes = len(df_clean)
    df_clean = limpiar_duplicados(df_clean)
    print(f"3. Duplicados eliminados: {registros_antes - len(df_clean)}")
    
    registros_antes = len(df_clean)
    df_clean = limpiar_fechas_inconsistentes(df_clean)
    print(f"4. Fechas inconsistentes eliminadas: {registros_antes - len(df_clean)}")
    
    registros_antes = len(df_clean)
    df_clean = limpiar_outliers(df_clean)
    print(f"5. Outliers eliminados: {registros_antes - len(df_clean)}")
    
    print(f"\nRegistros finales: {len(df_clean)}")
    print(f"Registros eliminados totales: {len(df) - len(df_clean)}")
    
    return df_clean


def generar_reporte_limpieza(df_original, df_limpio):
    """
    Genera reporte comparativo antes y después de la limpieza.
    """
    reporte = {
        'registros_originales': len(df_original),
        'registros_limpios': len(df_limpio),
        'registros_eliminados': len(df_original) - len(df_limpio),
        'porcentaje_retenido': (len(df_limpio) / len(df_original)) * 100,
        'valores_faltantes_antes': df_original.isnull().sum().sum(),
        'valores_faltantes_despues': df_limpio.isnull().sum().sum()
    }
    
    return reporte
