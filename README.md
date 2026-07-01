# Ecommerce ETL Python

## 📋 Objetivo

Este proyecto implementa un proceso **ETL (Extract, Transform, Load)** para analizar datos de una plataforma de ecommerce. El script realiza la extracción, limpieza y transformación de múltiples archivos CSV, y responde preguntas clave de negocio generando reportes en formato CSV y Parquet.

### Preguntas de negocio respondidas:
1. **¿Cuáles son los 5 clientes que más gastaron?**
2. **¿Cuál es el producto más vendido (por cantidad)?**
3. **¿Cómo evolucionaron las ventas mes a mes?**

---

## 📁 Estructura de Carpetas

```
ecommerce-etl-python/
│
├── etl.py                          # Script principal del ETL
├── README.md                       # Este archivo
│
├── data/                           # Carpeta con archivos CSV de entrada
│   ├── ecommerce_brands.csv
│   ├── ecommerce_categories.csv
│   ├── ecommerce_customers.csv
│   ├── ecommerce_inventory.csv
│   ├── ecommerce_orders.csv
│   ├── ecommerce_order_items.csv
│   ├── ecommerce_products.csv
│   ├── ecommerce_promotions.csv
│   ├── ecommerce_reviews.csv
│   ├── ecommerce_suppliers.csv
│   └── ecommerce_warehouses.csv
│
└── output/                         # Carpeta generada automáticamente con resultados
    ├── top_five_customers.csv
    ├── top_five_customers.parquet
    ├── producto_mas_vendido.csv
    ├── producto_mas_vendido.parquet
    ├── ventas_mes.csv
    └── ventas_mes.parquet
```

---

## 🛠️ Instalación de Dependencias

### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el proyecto:**
```bash
git clone https://github.com/marcosperez85/ecommerce-etl.git
cd ecommerce-etl-python
```

2. **Crear un entorno virtual (recomendado):**
```bash
python -m venv venv
```

3. **Activar el entorno virtual:**

   **En Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **En macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Instalar las dependencias:**
Las mismas se encuentran en `requirements.txt`:
```bash
pip install -r requirements.txt
```
---

## ▶️ Forma de Ejecución

### Paso 1: Ejecutar el script
Desde la carpeta raíz del proyecto:

```bash
python etl.py
```

### Paso 2: Resultados
El script generará:
- Mensajes en consola con el análisis
- Una carpeta `output/` con 6 archivos (3 CSV + 3 Parquet)
- Comparación de tamaños entre formatos

---

## 📊 Proceso ETL Detallado

### **Fase Extract**
- Lee todos los archivos CSV desde la carpeta `data/`
- Los almacena en un diccionario de DataFrames

### **Fase Transform**
1. **Limpieza de nulos**: Elimina filas con valores faltantes en columnas clave
2. **Eliminación de duplicados**: Remueve registros duplicados, manteniendo los más recientes
3. **Corrección de tipos de datos**:
   - Fechas → `datetime`
   - Números enteros → `int64`
   - Booleanos → `bool`

### **Fase Load**
- Exporta resultados a CSV y Parquet
- Compara tamaños de archivo entre ambos formatos

---

## 📝 Notas Importantes

- Los valores nulos en algunas columnas se rellenan con 0 intencionalmente.
- El análisis realiza merges inteligentes entre tablas relacionadas.
- Parquet suele ser más compacto que CSV para grandes volúmenes de datos.

---

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| "No se encontraron archivos" | Verifica que los CSV están en la ruta especificada |
| `ModuleNotFoundError: pandas` | Ejecuta: `pip install pandas` |
| Error de permisos en `output/` | Asegúrate de tener permisos de escritura en la carpeta |

---

## 📚 Recursos adicionales

- [Documentación de Pandas](https://pandas.pydata.org/docs/)
- [Formato Parquet](https://parquet.apache.org/)
