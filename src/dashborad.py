# ============================================================
# 📦 DASHBOARD INTERACTIVO UX/UI – EDA TIEMPOS DE ENTREGA
# ============================================================

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================
# 1️⃣ CARGA DE DATOS
# =========================
df = pd.read_csv("dataset_clean.csv")

# =========================
# 2️⃣ PREPARACIÓN DE DATOS
# =========================
df["processing_group"] = pd.cut(
    df["processing_days"],
    bins=[0, 1, 2, 3, 5, 10],
    labels=["≤1 día", "2 días", "3 días", "4-5 días", ">5 días"]
)

# =========================
# 3️⃣ LAYOUT GENERAL
# =========================
fig = make_subplots(
    rows=5, cols=2,
    specs=[
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "indicator"}, {"type": "indicator"}],
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "heatmap"}],
        [{"colspan": 2, "type": "bar"}, None]
    ],
    vertical_spacing=0.08,
    subplot_titles=[
        "<b>⏱️ Tiempo promedio de entrega (días)</b>",
        "<b>📍 Mediana del tiempo de entrega</b>",
        "<b>📊 Variabilidad (desviación estándar)</b>",
        "<b>⚠️ Pedidos fuera de promesa (%)</b>",
        "<b>🚚 Comparación por transportista</b>",
        "<b>🌍 Comparación por región</b>",
        "<b>📦 Distancia vs tiempo de entrega</b>",
        "<b>🔗 Correlaciones clave</b>",
        "<b>🏭 Impacto del tiempo de procesamiento</b>"
    ]
)

# =========================
# 4️⃣ KPIs (MÁS GRANDES)
# =========================
fig.add_trace(go.Indicator(
    mode="number",
    value=df["actual_delivery_days"].mean(),
    title={"text": "<b>Promedio</b>"},
    number={"font": {"size": 52}}
), 1, 1)

fig.add_trace(go.Indicator(
    mode="number",
    value=df["actual_delivery_days"].median(),
    title={"text": "<b>Mediana</b>"},
    number={"font": {"size": 52}}
), 1, 2)

fig.add_trace(go.Indicator(
    mode="number",
    value=df["actual_delivery_days"].std(),
    title={"text": "<b>Desviación estándar</b>"},
    number={"font": {"size": 52}}
), 2, 1)

fig.add_trace(go.Indicator(
    mode="number",
    value=(df["actual_delivery_days"] > df["promised_delivery_days"]).mean() * 100,
    title={"text": "<b>Fuera de promesa</b>"},
    number={"suffix": "%", "font": {"size": 52}}
), 2, 2)

# =========================
# 5️⃣ TRANSPORTISTA
# =========================
carrier_avg = df.groupby("shipping_carrier")["actual_delivery_days"].mean().sort_values()

fig.add_trace(go.Bar(
    x=carrier_avg.values,
    y=carrier_avg.index,
    orientation="h",
    marker=dict(
        color=carrier_avg.values,
        colorscale="Blues",
        line=dict(color="#1f2937", width=0.6)
    ),
    hovertemplate="<b>%{y}</b><br>Días promedio: %{x:.2f}<extra></extra>"
), 3, 1)

fig.update_xaxes(title_text="<b>Días promedio</b>", row=3, col=1)
fig.update_yaxes(title_text="<b>Transportista</b>", row=3, col=1)

# =========================
# 6️⃣ REGIÓN (GRIS UX)
# =========================
region_avg = df.groupby("customer_region")["actual_delivery_days"].mean().sort_values()

fig.add_trace(go.Bar(
    x=region_avg.index,
    y=region_avg.values,
    marker=dict(
        color="#b3b3b3",
        line=dict(color="#4b5563", width=0.9)
    ),
    hovertemplate="<b>Región:</b> %{x}<br><b>Días:</b> %{y:.2f}<extra></extra>",
    hoverlabel=dict(bgcolor="#4b5563", font_color="white")
), 3, 2)

fig.update_xaxes(title_text="<b>Región</b>", row=3, col=2)
fig.update_yaxes(title_text="<b>Días promedio</b>", row=3, col=2)

# =========================
# 7️⃣ SCATTER DISTANCIA
# =========================
fig.add_trace(go.Scatter(
    x=df["distance_km"],
    y=df["actual_delivery_days"],
    mode="markers",
    marker=dict(
        size=7,
        color=df["processing_days"],
        colorscale="Viridis",
        opacity=0.65,
        showscale=True,
        colorbar=dict(title="<b>Días<br>proc.</b>")
    ),
    hovertemplate="Distancia: %{x} km<br>Entrega: %{y} días<extra></extra>"
), 4, 1)

fig.update_xaxes(title_text="<b>Distancia (km)</b>", row=4, col=1)
fig.update_yaxes(title_text="<b>Días de entrega</b>", row=4, col=1)

# =========================
# 8️⃣ CORRELACIONES
# =========================
corr_vars = [
    "actual_delivery_days",
    "processing_days",
    "distance_km",
    "product_weight_kg",
    "shipping_cost_mxn"
]
corr = df[corr_vars].corr()

fig.add_trace(go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale="RdBu",
    zmid=0,
    text=corr.round(2).values,
    texttemplate="%{text}",
    hovertemplate="<b>%{x} vs %{y}</b><br>Corr: %{z:.2f}<extra></extra>"
), 4, 2)

# =========================
# 9️⃣ IMPACTO PROCESAMIENTO (ROJO VINO)
# =========================
proc_avg = df.groupby("processing_group")["actual_delivery_days"].mean()

fig.add_trace(go.Bar(
    x=proc_avg.index,
    y=proc_avg.values,
    marker=dict(
        color="#7f1d1d",
        line=dict(color="#3f0d0d", width=1)
    ),
    hovertemplate="<b>%{x}</b><br>Días: %{y:.2f}<extra></extra>",
    hoverlabel=dict(bgcolor="#3f0d0d", font_color="white")
), 5, 1)

fig.update_xaxes(title_text="<b>Tiempo de procesamiento</b>", row=5, col=1)
fig.update_yaxes(title_text="<b>Días promedio de entrega</b>", row=5, col=1)

# =========================
# 🔟 ESTILO FINAL
# =========================
fig.update_layout(
    title=dict(
        text="<b>📦 Dashboard UX – Análisis Exploratorio de Tiempos de Entrega</b>",
        x=0.5,
        font=dict(size=28)
    ),
    height=1900,
    template="plotly_white",
    showlegend=False,
    margin=dict(t=140, l=70, r=70)
)

# =========================
# 1️⃣1️⃣ EXPORTAR HTML
# =========================
fig.write_html("dashboard_eda_interactivo_ux.html", include_plotlyjs="cdn")

print("✅ Dashboard UX final generado correctamente")
