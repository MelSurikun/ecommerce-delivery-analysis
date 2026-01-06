import pandas as pd
import matplotlib.pyplot as plt

plt.style.use("ggplot")

df = pd.read_csv("dataset_clean.csv")

# 1️⃣ Histograma del tiempo de entrega
plt.figure()
plt.hist(df["delivery_days"], bins=30)
plt.title("Distribución del Tiempo de Entrega")
plt.xlabel("Tiempo de Entrega (días)")
plt.ylabel("Frecuencia")
plt.show()

# 2️⃣ Boxplot por tipo de envío
plt.figure()
df.boxplot(column="delivery_days", by="shipping_type")
plt.title("Tiempo de Entrega por Tipo de Envío")
plt.suptitle("")
plt.xlabel("Tipo de Envío")
plt.ylabel("Tiempo de Entrega (días)")
plt.show()

# 3️⃣ Scatter distancia vs tiempo
plt.figure()
plt.scatter(df["distance_km"], df["delivery_days"], alpha=0.5)
plt.title("Distancia vs Tiempo de Entrega")
plt.xlabel("Distancia (km)")
plt.ylabel("Tiempo de Entrega (días)")
plt.show()

# 4️⃣ Promedio por paquetería
promedio_paq = df.groupby("shipping_carrier")["delivery_days"].mean()

plt.figure()
promedio_paq.plot(kind="bar")
plt.title("Tiempo de Entrega Promedio por Paquetería")
plt.xlabel("Paquetería")
plt.ylabel("Tiempo Promedio (días)")
plt.show()

# 5️⃣ Heatmap de correlación
corr = df[["delivery_days", "distance_km", "processing_days", "quantity"]].corr()

plt.figure()
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Mapa de Correlación")
plt.show()

# 6️⃣ Boxplot por región
plt.figure()
df.boxplot(column="delivery_days", by="customer_region")
plt.title("Tiempo de Entrega por Región")
plt.suptitle("")
plt.xlabel("Región")
plt.ylabel("Tiempo de Entrega (días)")
plt.show()

# 7️⃣ Entregas rápidas vs lentas
df["categoria_tiempo"] = df["delivery_days"].apply(
    lambda x: "Rápida" if x <= 3 else "Lenta"
)

conteo = df["categoria_tiempo"].value_counts()

plt.figure()
plt.pie(conteo, labels=conteo.index, autopct="%1.1f%%")
plt.title("Proporción de Entregas Rápidas y Lentas")
plt.show()

# 8️⃣ Preparación vs tiempo
plt.figure()
plt.scatter(df["processing_days"], df["delivery_days"], alpha=0.5)
plt.title("Tiempo de Preparación vs Tiempo de Entrega")
plt.xlabel("Días de Preparación")
plt.ylabel("Tiempo de Entrega (días)")
plt.show()

# 9️⃣ Tiempo promedio por método de pago          
promedio_pago = df.groupby("payment_method")["delivery_days"].mean()

plt.figure()
promedio_pago.plot(kind="bar")
plt.title("Tiempo Promedio por Método de Pago")
plt.xlabel("Método de Pago")
plt.ylabel("Tiempo Promedio (días)")
plt.show()

# 🔟 Boxplot por cantidad de productos
plt.figure()
df.boxplot(column="delivery_days", by="quantity")
plt.title("Tiempo de Entrega según Cantidad de Productos")
plt.suptitle("")
plt.xlabel("Cantidad de Productos")
plt.ylabel("Tiempo de Entrega (días)")
plt.show()
