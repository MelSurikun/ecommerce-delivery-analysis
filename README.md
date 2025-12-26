## ecommerce-delivery-analysis

# EVALUACIÓN DE TIEMPO DE ENTREGA DE E-COMMERCE

Objetivo: Analizar qué factores aumentan o reducen el tiempo de entrega

Variables importantes a generar: fecha de envío, fecha de entrega, distancia, transportistas (catálogo de ellos como DHL, Estafeta, FEDEX, etc), peso de lo que se va a entregar o también puede ser peso y volumen.

Proceso: Calcular los días de entrega (rango entre fecha de envío y fecha de entrega), outliers, correlación entre las variables, métricas: tiempos promedios (por día o mes o año), la varianza por transportista, y la salida en gráficas, heatmap, análisis descriptivo, etc.

## Descripción del Proyecto
Análisis de datos simulados de ecommerce mexicano para identificar factores que afectan los tiempos de entrega y proponer mejoras en logística.

## Equipo
- **Persona 1**: [Melanie Hernández López] - Especialista en Datos & Generación
- **Persona 2**: [Nombre] - Ingeniero de Calidad & Limpieza
- **Persona 3**: [Nombre] - Analista Estadístico & EDA
- **Persona 4**: [Nombre] - Visualizador & Dashboard

## Objetivos
1. Generar dataset realista de 10k registros con 5% de errores controlados
2. Limpiar y validar la calidad de los datos
3. Analizar factores que afectan tiempos de entrega
4. Crear visualizaciones y dashboard interactivo

## Cómo Ejecutar
1. Clonar repositorio: `git clone [url]`
2. Crear entorno virtual: `python -m venv venv`
3. Activar entorno: `venv\Scripts\activate`
4. Instalar dependencias: `pip install -r requirements.txt`

En caso de que la carpeta "data" se encuentre vacía, ejecutar:
5. Generar datos: `python src/data_generation.py`