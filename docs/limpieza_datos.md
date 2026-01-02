# PROCESO DE LIMPIEZA DE DATOS
## Persona 2: Ingeniero de Calidad y Limpieza

### RESUMEN EJECUTIVO
- Dataset original: 10,000 registros
- Dataset limpio: 9,515 registros  
- Registros eliminados: 485 (4.85%)
- Retención: 95.15%

### ERRORES DETECTADOS Y CORREGIDOS

#### 1. VALORES FALTANTES (97 valores)
- Columnas: product_price_mxn, shipping_cost_mxn, distance_km, customer_loyalty_months
- Método: Imputación con mediana
- Acción: Corregidos (no eliminados)

#### 2. TYPOS (8 registros)
- Problema: Espacios extra en nombres de transportistas
- Ejemplos: ' FedEx', ' DHL', ' Estafeta'
- Método: str.strip()
- Acción: Corregidos (no eliminados)

#### 3. DUPLICADOS (0 registros)
- Criterio: order_id único
- Resultado: No encontrados en dataset

#### 4. FECHAS INCONSISTENTES (104 registros)
- Problemas: shipped_date < order_date, delivered_date < shipped_date
- Método: Validación lógica temporal
- Acción: Eliminados

#### 5. OUTLIERS (381 registros)
- Criterio: IQR con factor 3 (conservador)
- Detección: Precios y distancias superiores a Q3 + 3*IQR
- Ejemplos: Precios x100, distancias 5000-10000 km
- Acción: Eliminados

### FUNCIONES IMPLEMENTADAS
Módulo: `src/data_cleaning.py`

|               Función               | Descripción                |
|-------------------------------------|----------------------------|
| `limpiar_valores_faltantes()`       | Imputa con mediana         |
| `limpiar_typos_transportistas()`    | Elimina espacios           |
| `limpiar_duplicados()`              | Elimina por order_id       |
| `limpiar_fechas_inconsistentes()`   | Valida secuencia temporal  |
| `limpiar_outliers()`                | Detecta por IQR x3         |
| `limpiar_dataset_completo()`        | Aplica todas las limpiezas |
| `generar_reporte_limpieza()`        | Genera estadísticas        |

### ARCHIVOS GENERADOS
- Input: `data/raw/dataset_raw.csv` (10,000)
- Output: `data/processed/dataset_clean.csv` (9,515)
- Notebook: `notebooks/03_data_cleaning_process.ipynb`
- Módulo: `src/data_cleaning.py`

### CALIDAD FINAL
- Valores faltantes: 0
- Duplicados: 0
- Fechas válidas: 100%
- Outliers extremos: Eliminados
- Transportistas: 7 únicos sin typos

### DECISIÓN TÉCNICA: IQR x3
Factor 3 elegido sobre estándar 1.5 para:
- Eliminar solo outliers extremos
- Preservar variabilidad natural
- Alinearse con 5% de errores esperado
