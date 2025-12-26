# CAMBIOS DE GENERACIÓN DE DATOS
## Persona 1: [MELANIE]

### DISTRIBUCIONES IMPLEMENTADAS

#### TRANSPORTISTAS (Basado en mercado real):
- Estafeta: 28% - Más común en ecommerce
- DHL: 22% - Más rápido pero caro
- Correos de México: 15% - Económico pero lento
- FedEx: 18%, UPS: 10%, Redpack: 5%, Paquetexpress: 2%

#### TIEMPOS DE ENTREGA POR TRANSPORTISTA:
| Transportista | Local | Regional | Nacional | Notas |
|--------------|-------|----------|----------|-------|
| DHL          | 1 día | 2 días   | 3 días   | Más rápido |
| Estafeta     | 2 días| 4 días   | 6 días   | Balanceado |
| Correos      | 5 días| 8 días   | 12 días  | Más lento |

#### IMPACTO TEMPORADA ALTA:
- Hot Sale (Mayo), Buen Fin (Nov), Navidad (Dic)
- Multiplicador: 1.2x a 2.0x más tiempo
- Mayor probabilidad de problemas de entrega

#### ERRORES CONTROLADOS (5% = 500 registros):
1. **Missing values (20%)**: NaN en precio, costo envío, lealtad
2. **Outliers (20%)**: Precios 100x mayores, distancias imposibles
3. **Typos (20%)**: Espacios en transportistas, minúsculas/mayúsculas
4. **Duplicates (20%)**: Registros duplicados con order_id modificado
5. **Inconsistencias (20%)**: Fechas imposibles (entrega antes de envío)

### JUSTIFICACIÓN DE DECISIONES
- **Semilla 42**: Para reproducibilidad exacta
- **10,000 registros**: Suficiente para análisis estadístico
- **39 variables**: Cubren todas las dimensiones del problema
- **Errores 5%**: Realista para datos de ecommerce real