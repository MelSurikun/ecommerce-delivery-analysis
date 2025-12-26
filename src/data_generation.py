"""
GENERADOR DE DATOS DE ECOMMERCE MEXICANO
Autor: [Melanie] - Persona 1: Especialista en Datos & Generación
Fecha: [25/12/25]

DESCRIPCIÓN:
Genera dataset realista de ecommerce en México con 10,000 registros
y 5% de errores controlados para análisis de tiempos de entrega.

CARACTERÍSTICAS:
- 39 variables basadas en investigación del mercado mexicano
- Distribuciones realistas por transportista (DHL, Estafeta, Correos, etc.)
- Errores controlados: faltantes, outliers, typos, duplicados, inconsistencias
- Semilla 42 para reproducibilidad

USO:
python src/data_generation.py
Genera: data/raw/dataset_raw.csv (10k) y data/raw/dataset_sample_1000.csv

VARIABLES CLAVE:
- delivery_delay_days: Diferencia entre días prometidos y reales
- delivery_met_promise: 1 si llegó a tiempo, 0 si no
- customer_delivery_rating: Calificación 1-5 de la entrega
- shipping_carrier: Transportista (DHL más rápido, Correos más lento)

ANÁLISIS POSIBLE:
- ¿Qué transportista tiene mayor porcentaje de entregas a tiempo?
- ¿Cómo afectan las temporadas altas (Hot Sale) a los retrasos?
- ¿Los clientes leales reciben mejor servicio?
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
class MexicoEcommerceGenerator:
    def __init__(self, seed: int = 42, n_records: int = 10000):
        """
        Inicializa el generador con configuraciones para México
        
        Args:
            seed: Semilla para reproducibilidad
            n_records: Número de registros a generar
        """
        self.seed = seed
        self.n_records = n_records
        
        # Configurar semillas
        np.random.seed(seed)
        random.seed(seed)
        self.fake = Faker('es_MX')
        
        # Datos específicos de México
        self._setup_mexico_data()
        
    def _setup_mexico_data(self):
        """Configura datos reales de México basados en tu investigación"""
        
        # 1. ESTADOS Y REGIONES (32 estados reales)
        self.estados_mexico = [
            'Aguascalientes', 'Baja California', 'Baja California Sur',
            'Campeche', 'Chiapas', 'Chihuahua', 'Coahuila', 'Colima',
            'Ciudad de México', 'Durango', 'Guanajuato', 'Guerrero',
            'Hidalgo', 'Jalisco', 'México', 'Michoacán', 'Morelos',
            'Nayarit', 'Nuevo León', 'Oaxaca', 'Puebla', 'Querétaro',
            'Quintana Roo', 'San Luis Potosí', 'Sinaloa', 'Sonora',
            'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatán',
            'Zacatecas'
        ]
        
        # 2. REGIONES (agrupación para análisis)
        self.regiones = {
            'Centro': ['Ciudad de México', 'México', 'Puebla', 'Morelos', 
                      'Tlaxcala', 'Hidalgo', 'Querétaro'],
            'Norte': ['Nuevo León', 'Chihuahua', 'Coahuila', 'Sonora', 
                     'Tamaulipas', 'Baja California', 'Baja California Sur'],
            'Occidente': ['Jalisco', 'Michoacán', 'Guanajuato', 'Aguascalientes',
                         'Colima', 'Nayarit', 'Sinaloa'],
            'Sur': ['Guerrero', 'Oaxaca', 'Chiapas', 'Veracruz', 'Tabasco'],
            'Península': ['Yucatán', 'Quintana Roo', 'Campeche']
        }
        
        # 3. TRANSPORTISTAS MEXICANOS (con distribución real)
        self.transportistas = {
            'Estafeta': {'prob': 0.28, 'costo_base': 120, 'velocidad': 0.7},
            'DHL': {'prob': 0.22, 'costo_base': 180, 'velocidad': 0.9},
            'FedEx': {'prob': 0.18, 'costo_base': 160, 'velocidad': 0.8},
            'Correos de México': {'prob': 0.15, 'costo_base': 80, 'velocidad': 0.4},
            'UPS': {'prob': 0.10, 'costo_base': 170, 'velocidad': 0.85},
            'Redpack': {'prob': 0.05, 'costo_base': 100, 'velocidad': 0.6},
            'Paquetexpress': {'prob': 0.02, 'costo_base': 90, 'velocidad': 0.65}
        }
        
        # 4. CATEGORÍAS DE PRODUCTOS (AMVO 2024)
        self.categorias = {
            'Moda y Accesorios': {'prob': 0.25, 'precio_min': 150, 'precio_max': 5000},
            'Electrónicos': {'prob': 0.24, 'precio_min': 500, 'precio_max': 35000},
            'Hogar y Jardín': {'prob': 0.16, 'precio_min': 200, 'precio_max': 15000},
            'Salud y Belleza': {'prob': 0.12, 'precio_min': 100, 'precio_max': 3000},
            'Deportes': {'prob': 0.09, 'precio_min': 300, 'precio_max': 8000},
            'Libros y Educación': {'prob': 0.08, 'precio_min': 50, 'precio_max': 2000},
            'Juguetes y Bebés': {'prob': 0.06, 'precio_min': 200, 'precio_max': 4000}
        }
        
        # 5. MÉTODOS DE PAGO (datos reales de México)
        self.metodos_pago = {
            'Tarjeta de Débito': {'prob': 0.48, 'monto_share': 0.48},
            'Tarjeta de Crédito': {'prob': 0.30, 'monto_share': 0.52},
            'Efectivo (OXXO)': {'prob': 0.15, 'monto_share': 0.00},
            'PayPal': {'prob': 0.05, 'monto_share': 0.00},
            'Transferencia': {'prob': 0.02, 'monto_share': 0.00}
        }
        
        # 6. CANALES DE VENTA
        self.canales_venta = {
            'Mercado Libre': 0.35,
            'Amazon México': 0.25,
            'Liverpool': 0.10,
            'Coppel': 0.08,
            'Walmart': 0.07,
            'Sitio Web Propio': 0.15
        }
        
        # 7. TIEMPOS DE ENTREGA BASE (días hábiles)
        self.tiempos_base = {
            'Estafeta': {'local': 2, 'regional': 4, 'nacional': 6},
            'DHL': {'local': 1, 'regional': 2, 'nacional': 3},
            'FedEx': {'local': 2, 'regional': 3, 'nacional': 4},
            'Correos de México': {'local': 5, 'regional': 8, 'nacional': 12},
            'UPS': {'local': 1, 'regional': 2, 'nacional': 4},
            'Redpack': {'local': 3, 'regional': 5, 'nacional': 7},
            'Paquetexpress': {'local': 3, 'regional': 5, 'nacional': 8}
        }
    
    # ============================================================================
    # FUNCIONES DE GENERACIÓN
    # ============================================================================
    
    def _get_random_transportista(self) -> str:
        """Selecciona transportista según distribución real"""
        transportistas = list(self.transportistas.keys())
        probabilidades = [self.transportistas[t]['prob'] for t in transportistas]
        return np.random.choice(transportistas, p=probabilidades)
    
    def _get_random_categoria(self) -> str:
        """Selecciona categoría según distribución real"""
        categorias = list(self.categorias.keys())
        probabilidades = [self.categorias[c]['prob'] for c in categorias]
        return np.random.choice(categorias, p=probabilidades)
    
    def _get_region_from_estado(self, estado: str) -> str:
        """Obtiene la región a partir del estado"""
        for region, estados in self.regiones.items():
            if estado in estados:
                return region
        return 'Centro'  # Default
    
    def _calcular_tiempo_entrega(self, transportista: str, estado_origen: str, 
                                 estado_destino: str, es_temporada_alta: bool) -> int:
        """
        Calcula tiempo de entrega realista considerando:
        - Transportista
        - Distancia (mismo estado, región diferente, nacional)
        - Temporada alta
        """
        
        # Determinar tipo de envío por distancia
        if estado_origen == estado_destino:
            tipo_envio = 'local'
        elif self._get_region_from_estado(estado_origen) == self._get_region_from_estado(estado_destino):
            tipo_envio = 'regional'
        else:
            tipo_envio = 'nacional'
        
        # Tiempo base según transportista y tipo
        tiempo_base = self.tiempos_base[transportista][tipo_envio]
        
        # Variabilidad natural (distribución normal)
        variabilidad = np.random.normal(0, 0.5)  # +/- 0.5 días
        
        # Impacto de temporada alta (Hot Sale, Buen Fin, Navidad)
        if es_temporada_alta:
            impacto_temporada = np.random.uniform(1.2, 2.0)  # 20-100% más lento
        else:
            impacto_temporada = 1.0
        
        # Cálculo final (mínimo 1 día) - CONVERTIR explícitamente a int
        tiempo_final = max(1, int(round(float(tiempo_base * impacto_temporada + variabilidad))))
        
        return tiempo_final
    
    def _es_temporada_alta(self, fecha: datetime) -> bool:
        """Determina si la fecha está en temporada alta mexicana"""
        mes = fecha.month
        
        # Hot Sale: Mayo
        # Buen Fin: Noviembre
        # Navidad: Diciembre
        # Día del Niño: Abril
        # 14 Febrero: Febrero
        
        if mes == 5 or mes == 11 or mes == 12:  # Hot Sale, Buen Fin, Navidad
            return True
        elif mes == 4 and fecha.day == 30:  # Día del Niño
            return True
        elif mes == 2 and fecha.day == 14:  # 14 Febrero
            return True
        else:
            return False
    
    def _generar_fechas_realistas(self, transportista: str, estado_destino: str) -> Dict:
        """
        Genera fechas realistas para el proceso de compra
        """
        # Fecha de pedido (último año)
        fecha_pedido = self.fake.date_time_between(start_date='-1y', end_date='now')
        
        # Días para procesar el pedido (1-3 días normalmente)
        # CONVERTIR a int explícitamente para timedelta
        dias_procesamiento_opciones = [1, 2, 3]
        dias_procesamiento = int(np.random.choice(dias_procesamiento_opciones, p=[0.7, 0.2, 0.1]))
        fecha_envio = fecha_pedido + timedelta(days=dias_procesamiento)
        
        # Determinar si es temporada alta
        es_temporada_alta = self._es_temporada_alta(fecha_pedido)
        
        # Estado origen (simulado como CDMX para simplificar)
        estado_origen = 'Ciudad de México'
        
        # Calcular tiempo de entrega
        dias_entrega = self._calcular_tiempo_entrega(
            transportista, estado_origen, estado_destino, es_temporada_alta
        )
        
        # Añadir variabilidad final
        dias_entrega += int(np.random.randint(-1, 2))  # +/- 1 día, CONVERTIR a int
        
        fecha_entrega = fecha_envio + timedelta(days=max(1, dias_entrega))
        
        return {
            'order_date': fecha_pedido,
            'shipped_date': fecha_envio,
            'delivered_date': fecha_entrega,
            'processing_days': dias_procesamiento,
            'delivery_days': dias_entrega
        }
    
    def _generar_datos_producto(self, categoria: str) -> Dict:
        """Genera datos realistas del producto"""
        cat_info = self.categorias[categoria]
        
        # Precio según categoría
        precio = np.random.uniform(cat_info['precio_min'], cat_info['precio_max'])
        
        # Peso según categoría (kg)
        if categoria == 'Electrónicos':
            peso = np.random.uniform(0.5, 5.0)
        elif categoria == 'Moda y Accesorios':
            peso = np.random.uniform(0.1, 2.0)
        elif categoria == 'Hogar y Jardín':
            peso = np.random.uniform(1.0, 15.0)
        else:
            peso = np.random.uniform(0.2, 3.0)
        
        # Cantidad (1-5 normalmente, 6-10 ocasionalmente para reabastecimiento)
        if np.random.random() < 0.95:
            cantidad = int(np.random.randint(1, 6))
        else:
            cantidad = int(np.random.randint(6, 11))
        
        return {
            'product_price_mxn': round(float(precio), 2),
            'product_weight_kg': round(float(peso), 2),
            'quantity': cantidad
        }
    
    def _generar_datos_cliente(self) -> Dict:
        """Genera datos del cliente"""
        # Grupo de edad basado en distribución real
        grupos_edad = ['18-24', '25-34', '35-44', '45-54', '55+']
        prob_grupos = [0.15, 0.35, 0.25, 0.15, 0.10]
        edad_grupo = np.random.choice(grupos_edad, p=prob_grupos)
        
        # Lealtad del cliente (meses)
        lealtad_meses = np.random.exponential(scale=12)  # Media de 1 año
        lealtad_meses = min(int(lealtad_meses), 60)  # Máximo 5 años
        
        # Frecuencia de compra (compras por mes)
        frecuencia = int(np.random.poisson(lam=2.5))  # Media de 2.5 compras/mes
        
        return {
            'customer_age_group': edad_grupo,
            'customer_loyalty_months': lealtad_meses,
            'purchase_frequency': frecuencia
        }
    
    def _generar_datos_pago(self, monto_total: float) -> Dict:
        """Genera datos de pago realistas para México"""
        metodos = list(self.metodos_pago.keys())
        probabilidades = [self.metodos_pago[m]['prob'] for m in metodos]
        metodo = np.random.choice(metodos, p=probabilidades)
        
        # Status de transacción (67% aprobadas según datos)
        if np.random.random() < 0.67:
            status = 'Autorizada'
        elif np.random.random() < 0.8:
            status = 'En revisión'
        else:
            status = 'Rechazada'
        
        # Meses sin intereses (solo para tarjeta de crédito)
        if metodo == 'Tarjeta de Crédito' and status == 'Autorizada':
            msi_opciones = [1, 3, 6, 12, 18]
            msi = int(np.random.choice(msi_opciones, p=[0.3, 0.25, 0.2, 0.15, 0.1]))
        else:
            msi = 1
        
        return {
            'payment_method': metodo,
            'transaction_status': status,
            'payment_installments': msi
        }
    
    def _calcular_costo_envio(self, transportista: str, peso: float, 
                             distancia: str, es_express: bool) -> float:
        """Calcula costo de envío realista"""
        costo_base = self.transportistas[transportista]['costo_base']
        
        # Ajuste por peso (MXN por kg)
        costo_peso = peso * 15
        
        # Ajuste por distancia
        if distancia == 'local':
            ajuste_distancia = 1.0
        elif distancia == 'regional':
            ajuste_distancia = 1.5
        else:  # nacional
            ajuste_distancia = 2.0
        
        # Ajuste por servicio express
        if es_express:
            ajuste_express = 2.0
        else:
            ajuste_express = 1.0
        
        # Cálculo final
        costo_final = (costo_base + costo_peso) * ajuste_distancia * ajuste_express
        
        # Variabilidad aleatoria +/- 10%
        variacion = np.random.uniform(0.9, 1.1)
        
        return round(float(costo_final * variacion), 2)
    
    def _agregar_errores_controlados(self, df: pd.DataFrame, porcentaje: float = 0.05) -> pd.DataFrame:
        """
        Agrega errores controlados al 5% de los datos
        Tipos de errores implementados:
        1. Valores faltantes
        2. Outliers extremos
        3. Errores de tipeo
        4. Duplicados
        5. Inconsistencias
        """
        df_con_errores = df.copy()
        n_errores = int(len(df) * porcentaje)
        indices_errores = np.random.choice(df.index, n_errores, replace=False)
        
        for idx in indices_errores:
            tipo_error = np.random.choice(['missing', 'outlier', 'typo', 'duplicate', 'inconsistent'])
            
            if tipo_error == 'missing':
                # Valores faltantes en columnas importantes
                columna = np.random.choice(['product_price_mxn', 'shipping_cost_mxn', 
                                           'customer_loyalty_months', 'distance_km'])
                df_con_errores.at[idx, columna] = np.nan
                
            elif tipo_error == 'outlier':
                # Valores extremadamente altos o bajos
                if np.random.random() > 0.5:
                    # Precio 100x mayor
                    df_con_errores.at[idx, 'product_price_mxn'] = float(df_con_errores.at[idx, 'product_price_mxn']) * 100
                else:
                    # Distancia imposible
                    df_con_errores.at[idx, 'distance_km'] = int(np.random.randint(5000, 10000))
                    
            elif tipo_error == 'typo':
                # Errores de escritura
                if np.random.random() > 0.5:
                    # Espacios extra en transportista
                    df_con_errores.at[idx, 'shipping_carrier'] = ' ' + str(df_con_errores.at[idx, 'shipping_carrier'])
                else:
                    # Minúsculas donde deberían ser mayúsculas
                    df_con_errores.at[idx, 'customer_state'] = str(df_con_errores.at[idx, 'customer_state']).lower()
                    
            elif tipo_error == 'duplicate':
                # Duplicar registro anterior (pero con diferente order_id)
                if idx > 0:
                    df_con_errores.iloc[idx] = df_con_errores.iloc[idx-1]
                    # Cambiar order_id para no ser exactamente igual
                    original_id = df_con_errores.at[idx, 'order_id']
                    df_con_errores.at[idx, 'order_id'] = f"DUPE-{original_id}"
                    
            elif tipo_error == 'inconsistent':
                # Fechas inconsistentes
                if np.random.random() > 0.5:
                    # Entrega antes del envío
                    df_con_errores.at[idx, 'delivered_date'] = (
                        df_con_errores.at[idx, 'shipped_date'] - timedelta(days=2)
                    )
                else:
                    # Envío antes del pedido
                    df_con_errores.at[idx, 'shipped_date'] = (
                        df_con_errores.at[idx, 'order_date'] - timedelta(days=1)
                    )
        
        return df_con_errores
    
    # ============================================================================
    # MÉTODO PRINCIPAL
    # ============================================================================
    
    def generate_dataset(self, include_errors: bool = True) -> pd.DataFrame:
        """
        Genera el dataset completo de ecommerce mexicano
        
        Args:
            include_errors: Si True, incluye 5% de datos con errores controlados
            
        Returns:
            DataFrame con los datos generados
        """
        print(f"Generando {self.n_records} registros de ecommerce mexicano...")
        
        datos = []
        
        for i in range(self.n_records):
            # 1. IDENTIFICACIÓN
            order_id = f"ECOMMX-2024-{i:05d}"
            customer_id = f"CUST-{self.fake.random_int(10000, 99999)}"
            
            # 2. CLIENTE
            datos_cliente = self._generar_datos_cliente()
            estado_cliente = np.random.choice(self.estados_mexico)
            region_cliente = self._get_region_from_estado(estado_cliente)
            
            # 3. PRODUCTO
            categoria = self._get_random_categoria()
            datos_producto = self._generar_datos_producto(categoria)
            
            # 4. TRANSPORTISTA Y LOGÍSTICA
            transportista = self._get_random_transportista()
            
            # Determinar si es envío express (15% probabilidad)
            es_express = np.random.random() < 0.15
            
            # Generar fechas realistas
            fechas = self._generar_fechas_realistas(transportista, estado_cliente)
            
            # Calcular distancia (simulada)
            if estado_cliente == 'Ciudad de México':
                distancia_km = int(np.random.randint(0, 50))
                tipo_distancia = 'local'
            elif region_cliente == 'Centro':
                distancia_km = int(np.random.randint(50, 300))
                tipo_distancia = 'regional'
            else:
                distancia_km = int(np.random.randint(300, 1500))
                tipo_distancia = 'nacional'
            
            # Calcular costo de envío
            costo_envio = self._calcular_costo_envio(
                transportista, datos_producto['product_weight_kg'], 
                tipo_distancia, es_express
            )
            
            # 5. PAGO
            monto_total = datos_producto['product_price_mxn'] * datos_producto['quantity'] + costo_envio
            datos_pago = self._generar_datos_pago(float(monto_total))
            
            # 6. CANAL DE VENTA
            canales = list(self.canales_venta.keys())
            probabilidades = list(self.canales_venta.values())
            canal_venta = np.random.choice(canales, p=probabilidades)
            
            # 7. DÍAS PROMETIDOS vs REALES
            # Días prometidos: base según transportista, menos si es express
            dias_prometidos_base = self.tiempos_base[transportista][tipo_distancia]
            if es_express:
                dias_prometidos = max(1, dias_prometidos_base - 2)
            else:
                dias_prometidos = dias_prometidos_base
            
            dias_reales = (fechas['delivered_date'] - fechas['shipped_date']).days
            
            # 8. CALIFICACIÓN DEL CLIENTE (basada en experiencia)
            diferencia_dias = dias_reales - dias_prometidos
            
            if diferencia_dias <= 0:
                # Entrega a tiempo o temprana
                calificacion_base = 5
            elif diferencia_dias <= 2:
                # Retraso menor
                calificacion_base = 4
            elif diferencia_dias <= 5:
                # Retraso moderado
                calificacion_base = 3
            elif diferencia_dias <= 10:
                # Retraso significativo
                calificacion_base = 2
            else:
                # Retraso grave
                calificacion_base = 1
            
            # Añadir variabilidad aleatoria
            calificacion = max(1, min(5, calificacion_base + int(np.random.randint(-1, 2))))
            
            # 9. PROBLEMAS DE ENTREGA
            problemas = ['Ninguno', 'Retraso', 'Paquete dañado', 'Extraviado', 'Entregado en lugar equivocado']
            probabilidades_problemas = [0.85, 0.10, 0.03, 0.01, 0.01]
            
            # Más probabilidad de problemas si hay retraso
            if diferencia_dias > 2:
                probabilidades_problemas = [0.70, 0.20, 0.05, 0.03, 0.02]
            
            problema_entrega = np.random.choice(problemas, p=probabilidades_problemas)
            
            # 10. CREAR REGISTRO COMPLETO
            registro = {
                # Identificación
                'order_id': order_id,
                'customer_id': customer_id,
                
                # Fechas
                'order_date': fechas['order_date'],
                'shipped_date': fechas['shipped_date'],
                'delivered_date': fechas['delivered_date'],
                
                # Tiempos calculados
                'processing_days': fechas['processing_days'],
                'delivery_days': fechas['delivery_days'],
                'promised_delivery_days': dias_prometidos,
                'actual_delivery_days': dias_reales,
                'delivery_delay_days': diferencia_dias,
                'delivery_met_promise': 1 if diferencia_dias <= 0 else 0,
                
                # Producto
                'product_category': categoria,
                'product_price_mxn': datos_producto['product_price_mxn'],
                'product_weight_kg': datos_producto['product_weight_kg'],
                'quantity': datos_producto['quantity'],
                'total_amount_mxn': round(float(monto_total), 2),
                
                # Logística
                'shipping_carrier': transportista,
                'shipping_tier': 'Express' if es_express else 'Estándar',
                'shipping_cost_mxn': costo_envio,
                'distance_km': distancia_km,
                'shipping_type': tipo_distancia,
                
                # Cliente
                'customer_state': estado_cliente,
                'customer_region': region_cliente,
                'customer_age_group': datos_cliente['customer_age_group'],
                'customer_loyalty_months': datos_cliente['customer_loyalty_months'],
                'purchase_frequency': datos_cliente['purchase_frequency'],
                'is_urban': 1 if np.random.random() < 0.75 else 0,  # 75% urbano
                
                # Pago
                'payment_method': datos_pago['payment_method'],
                'transaction_status': datos_pago['transaction_status'],
                'payment_installments': datos_pago['payment_installments'],
                
                # Canal
                'sales_channel': 'Marketplace' if canal_venta != 'Sitio Web Propio' else 'D2C',
                'platform_name': canal_venta,
                
                # Temporada
                'is_peak_season': 1 if self._es_temporada_alta(fechas['order_date']) else 0,
                
                # Experiencia de entrega
                'customer_delivery_rating': calificacion,
                'delivery_issue': problema_entrega,
                
                # Variables derivadas (para análisis)
                'shipping_cost_to_price_ratio': round(float(costo_envio / datos_producto['product_price_mxn']), 4),
                'is_frequent_customer': 1 if datos_cliente['purchase_frequency'] > 3 else 0,
                'is_loyal_customer': 1 if datos_cliente['customer_loyalty_months'] > 12 else 0,
                'high_value_order': 1 if monto_total > 5000 else 0
            }
            
            datos.append(registro)
            
            # Mostrar progreso cada 1000 registros
            if (i + 1) % 1000 == 0:
                print(f"  Generados {i + 1}/{self.n_records} registros...")
        
        # Crear DataFrame
        df = pd.DataFrame(datos)
        
        # Añadir errores controlados si se solicita
        if include_errors:
            print("Añadiendo 5% de errores controlados...")
            df = self._agregar_errores_controlados(df, porcentaje=0.05)
        
        print("¡Dataset generado exitosamente!")
        return df
    
    def save_dataset(self, df: pd.DataFrame, filepath: str = 'data/raw/dataset_raw.csv'):
        """Guarda el dataset en un archivo CSV"""
        import os
        
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Guardar en CSV
        df.to_csv(filepath, index=False, encoding='utf-8')
        print(f"Dataset guardado en: {filepath}")
        print(f"Tamaño: {len(df)} registros, {len(df.columns)} columnas")
        
        return filepath

# ============================================================================
# FUNCIÓN PRINCIPAL PARA EJECUTAR
# ============================================================================

def main():
    """Función principal para generar y guardar el dataset"""
    
    print("=" * 60)
    print("GENERADOR DE DATOS DE ECOMMERCE MEXICANO")
    print("Persona 1: Especialista en Datos & Generación")
    print("=" * 60)
    
    # 1. Crear generador
    generator = MexicoEcommerceGenerator(
        seed=42,          # Para reproducibilidad
        n_records=10000   # 10,000 registros como requerido
    )
    
    # 2. Generar dataset
    df = generator.generate_dataset(include_errors=True)
    
    # 3. Mostrar información del dataset
    print("\n" + "=" * 60)
    print("INFORMACIÓN DEL DATASET GENERADO:")
    print("=" * 60)
    print(f"Registros totales: {len(df):,}")
    print(f"Columnas: {len(df.columns)}")
    print("\nPrimeras 5 filas:")
    print(df.head())
    print("\nColumnas disponibles:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # 4. Estadísticas básicas
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS BÁSICAS:")
    print("=" * 60)
    
    # Distribución de transportistas
    print("\nDistribución de transportistas:")
    dist_transp = df['shipping_carrier'].value_counts(normalize=True)
    for transp, porcentaje in dist_transp.items():
        print(f"  {transp:<20}: {porcentaje:.1%}")
    
    # Tiempos de entrega
    print(f"\nDías de entrega promedio: {df['actual_delivery_days'].mean():.1f}")
    print(f"Días de retraso promedio: {df['delivery_delay_days'].mean():.1f}")
    print(f"Porcentaje de entregas a tiempo: {df['delivery_met_promise'].mean():.1%}")
    
    # Calificación promedio
    print(f"Calificación promedio de entrega: {df['customer_delivery_rating'].mean():.1f}/5.0")
    
    # 5. Guardar dataset
    print("\n" + "=" * 60)
    print("GUARDANDO DATASET...")
    print("=" * 60)
    
    filepath = generator.save_dataset(df)
    
    print("\n" + "=" * 60)
    print("¡GENERACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print("\nArchivos generados:")
    print(f"  1. {filepath} (dataset principal)")
    print(f"  2. data/raw/dataset_sample_1000.csv (muestra para pruebas)")
    
    # 6. Crear una muestra más pequeña para pruebas rápidas
    if len(df) > 1000:
        sample_df = df.sample(1000, random_state=42)
        sample_path = 'data/raw/dataset_sample_1000.csv'
        sample_df.to_csv(sample_path, index=False, encoding='utf-8')
        print(f"  3. {sample_path} (muestra de 1,000 registros)")
    
    print("\n¡Listo para pasar a la Persona 2 (Limpieza de Datos)!")
    
    return df

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == "__main__":
    # Ejecutar la generación
    dataset = main()
    
    # Mostrar cómo cargarlo después
    print("\n" + "=" * 60)
    print("PARA CARGAR EL DATASET EN OTRO SCRIPT:")
    print("=" * 60)
    print("import pandas as pd")
    print("df = pd.read_csv('data/raw/dataset_raw.csv', parse_dates=['order_date', 'shipped_date', 'delivered_date'])")
    print("print(f'Dataset cargado: {len(df)} registros')")