# ecommerce-delivery-analysis

## EVALUACIÓN DE TIEMPO DE ENTREGA DE E-COMMERCE

Objetivo: Analizar qué factores aumentan o reducen el tiempo de entrega

Variables importantes a generar: fecha de envío, fecha de entrega, distancia, transportistas (catálogo de ellos como DHL, Estafeta, FEDEX, etc), peso de lo que se va a entregar o también puede ser peso y volumen.

Proceso: Calcular los días de entrega (rango entre fecha de envío y fecha de entrega), outliers, correlación entre las variables, métricas: tiempos promedios (por día o mes o año), la varianza por transportista, y la salida en gráficas, heatmap, análisis descriptivo, etc.

<div align="center">

### Stack Tecnológico
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-5A4B7F?style=for-the-badge&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37726?style=for-the-badge&logo=jupyter&logoColor=white)

</div>

---

## Descripción del Proyecto
Análisis de datos simulados de ecommerce mexicano para identificar factores que afectan los tiempos de entrega y proponer mejoras en logística.

---

## Equipo

<div align="center">

| Nombre | Rol |
|--------|-----|
| Melanie Hernández López | Especialista en Datos & Generación |
| Ángel David Reyes Calva | Ingeniero de Calidad & Limpieza |
| Byron Leonardo Ayala Velasco | Analista Estadístico & EDA |
| Leo Galvan Landan | Visualizador & Dashboard |

</div>

---

## Objetivos
1. Generar dataset realista de 10k registros con 5% de errores controlados
2. Limpiar y validar la calidad de los datos
3. Analizar factores que afectan tiempos de entrega
4. Crear visualizaciones y dashboard interactivo

---

## Cómo Ejecutar
1. Clonar repositorio: git clone https://github.com/MelSurikun/ecommerce-delivery-analysis.git
2. Crear entorno virtual: python -m venv venv
3. Activar entorno: venv\Scripts\activate
4. Instalar dependencias: pip install -r requirements.txt

En caso de que la carpeta "data" se encuentre vacía, ejecutar:
5. Generar datos: python src/data_generation.py

---

<div align="center">

### Tecnologías Utilizadas
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat)
![Pandas](https://img.shields.io/badge/pandas-2.0+-green?style=flat)
![NumPy](https://img.shields.io/badge/NumPy-latest-blue?style=flat)
![Matplotlib](https://img.shields.io/badge/Matplotlib-latest-blue?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-latest-blue?style=flat)
![SciPy](https://img.shields.io/badge/SciPy-latest-blue?style=flat)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat)

</div>