# PLAN DE VARIABLES - ECOMMERCE MÉXICO
## Persona 1 [Melanie]: Especialista en Datos & Generación

### CONTEXTO
Dataset generado para análisis de tiempos de entrega en ecommerce mexicano.
Basado en investigación de AMVO 2024 y datos reales del mercado.

### VARIABLES GENERADAS (39 totales)

#### 1. IDENTIFICACIÓN (2)
- `order_id`: ID único formato "ECOMMX-2024-XXXXX"
- `customer_id`: ID anónimo del cliente

#### 2. FECHAS Y TIEMPOS (8)
- `order_date`, `shipped_date`, `delivered_date`: Fechas reales
- `delivery_delay_days`: Días de retraso (prometido vs real) **VARIABLE CLAVE**
- `delivery_met_promise`: 1 si llegó a tiempo, 0 si no **VARIABLE OBJETIVO**

#### 3. PRODUCTO (5)
- `product_category`: 7 categorías basadas en AMVO 2024
- `product_price_mxn`: Precios realistas por categoría
- `product_weight_kg`: Peso realista para cálculo logístico

#### 4. LOGÍSTICA (6)
- `shipping_carrier`: 7 transportistas mexicanos con distribución real
- `shipping_tier`: "Estándar" (85%) vs "Express" (15%)
- `distance_km`: Distancia simulada CDMX -> Estado destino

#### 5. CLIENTE (6)
- `customer_state`: 32 estados de México reales
- `customer_age_group`: Grupos basados en distribución real
- `customer_loyalty_months`: Meses como cliente (media: 12 meses)

#### 6. ERRORES CONTROLADOS (5%)
Implementados en: precios, fechas, transportistas, valores faltantes
Tipos: missing, outlier, typo, duplicate, inconsistent