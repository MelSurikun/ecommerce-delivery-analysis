# visualization_notebook.py

import pandas as pd
import matplotlib.pyplot as plt

# Cargar dataset limpio
df = pd.read_csv("dataset_clean.csv")
df.columns = df.columns.str.strip()

# Convertir columnas numéricas
numericas = ["processing_days", "delivery_days", "promised_delivery_days",
             "actual_delivery_days", "delivery_delay_days", "product_price_mxn",
             "product_weight_kg", "quantity", "total_amount_mxn", "shipping_cost_mxn",
             "distance_km", "customer_loyalty_months", "purchase_frequency",
             "shipping_cost_to_price_ratio", "customer_delivery_rating"]

for col in numericas:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["delivery_days"])

# 1️⃣ Histograma de delivery_days
fig1 = px.histogram(df, x="delivery_days", nbins=30,
                    title="Distribución del Tiempo de Entrega",
                    labels={"delivery_days":"Tiempo de Entrega (días)"})
fig1.show()

# 2️⃣ Boxplot por tipo de envío
fig2 = px.box(df, x="shipping_type", y="delivery_days",
              title="Tiempo de Entrega por Tipo de Envío",
              labels={"shipping_type":"Tipo de Envío","delivery_days":"Tiempo de Entrega (días)"})
fig2.show()

# 3️⃣ Scatter distancia vs delivery_days
fig3 = px.scatter(df, x="distance_km", y="delivery_days",
                  color="shipping_type",
                  title="Distancia vs Tiempo de Entrega",
                  labels={"distance_km":"Distancia (km)","delivery_days":"Tiempo de Entrega (días)"})
fig3.show()

# 4️⃣ Tiempo promedio por carrier
promedio_carrier = df.groupby("shipping_carrier")["delivery_days"].mean().reset_index()
fig4 = px.bar(promedio_carrier, x="shipping_carrier", y="delivery_days",
              title="Tiempo de Entrega Promedio por Paquetería",
              labels={"shipping_carrier":"Paquetería","delivery_days":"Promedio (días)"})
fig4.show()

# 5️⃣ Boxplot por categoría de producto
fig5 = px.box(df, x="product_category", y="delivery_days",
              title="Tiempo de Entrega según Categoría de Producto",
              labels={"product_category":"Categoría de Producto","delivery_days":"Tiempo de Entrega (días)"})
fig5.show()

# 6️⃣ Pie entregas cumplidas vs retrasadas
fig6 = px.pie(df, names="delivery_met_promise", title="Entregas que Cumplieron Promesa vs Retrasadas")
fig6.show()

# 7️⃣ Boxplot por día de la semana
df["order_day"] = pd.to_datetime(df["order_date"]).dt.day_name()
fig7 = px.box(df, x="order_day", y="delivery_days",
              title="Tiempo de Entrega por Día de la Semana",
              labels={"order_day":"Día de la Semana","delivery_days":"Tiempo de Entrega (días)"})
fig7.show()

# 8️⃣ Scatter 3D: distancia, processing_days, delivery_days
fig8 = px.scatter_3d(df, x="distance_km", y="processing_days", z="delivery_days",
                     color="shipping_type", title="3D: Distancia, Procesamiento y Tiempo de Entrega")
fig8.show()
