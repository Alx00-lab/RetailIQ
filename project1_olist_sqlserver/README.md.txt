Descripción
Este toolkit es una solución modular diseñada en Python + Pandas para automatizar el proceso de Exploratory Data Analysis (EDA) y control de calidad. Permite diagnosticar rápidamente la integridad de múltiples conjuntos de datos, detectar inconsistencias lógicas y normalizar tipos de datos para su posterior análisis o modelado.

🚀 Funcionalidades Principales
1. Auditoría Automatizada de Tablas
El script itera sobre diccionarios de DataFrames para generar un reporte instantáneo que incluye:

Dimensiones: Conteo exacto de filas y columnas (shape).

Integridad: Detección de valores nulos por columna.

Tipado: Verificación de tipos de datos (dtypes).

Unicidad: Identificación de registros duplicados.

2. Validación de Reglas de Negocio
Incluye filtros lógicos para detectar valores inválidos o fuera de rango, tales como:

Precios iguales a cero o negativos (price <= 0).

Validación de consistencia en IDs o categorías.

3. Normalización Temporal
Automatiza la conversión de objetos de texto a objetos datetime64[ns], facilitando:

Extracción de componentes (Año, Mes, Día).

Cálculo de deltas de tiempo.

Análisis de series temporales.