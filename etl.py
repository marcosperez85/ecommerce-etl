import pandas as pd
import os
import glob

# Usamos glob para obtener todos los archivos CSV en una carpeta
directory = r"\Marcos\Programacion\ecommerce-etl-python\data"
file_list = os.listdir(directory)
csv_files = glob.glob(os.path.join(directory, '*.csv'))

if not csv_files:
    print(f"No se encontraron los archivos en la ruta especificada\n")
else:
    print(f"Cantidad de archivos encontrados: {len(csv_files)}\n")

columnas_de_integer = ["founded_year", "display_order", "product_id", "warehouse_id", "quantity", "min_stock_level", "max_stock_level", "order_id", "category_id", "brand_id", "supplier_id", "customer_id", "capacity_units", "helpful_votes", "current_occupancy"]
columnas_de_boolean = ["is_verified_purchase", "is_verified", "is_active", "accepts_marketing", "is_premium"]
columnas_de_fechas = ["birth_date", "registration_date", "last_login", "last_restock_date", "order_date", "created_at", "updated_at", "start_date" ,"end_date"]

# Funciones que vamos a usar luego

# ============================================================================================================
def mostrar_datos(df):
    # Mostrar info de cada archivo dentro del array
    # No uso range(0,10) en zip() para no hardcodear la cantidad de archivos
    
    print(f"*** Informacion de {os.path.basename(file)} ***\n")
    # print(f"Cantidad de filas: {len(df)}, cantidad de columnas: {len(df.columns)}\n")
    # print(df.head())
    # df.info()

# ============================================================================================================
def eliminar_nulos(df):    
    # Tener cuidado de no eliminar nulos o intentar rellenar sin criterio aquellas columnas donde no
    # tenga sentido para el contexto de lo que representa el dataframe

    # No usar print(df.isnull()) sin .sum() porque evalua cada celda del dataframe y me devuelve el dataframe
    # entero pero indicando true/false en cada celda
    
    # Este comando en cambio me da un recuento de los Nulls de cada columna
    # print(f"Recuento de valores nulos por cada columna (ANTES DE LIMPIAR):\n")
    # print(df.isnull().sum())

    if "product_id" in df.columns:
        df = df.dropna(subset=["product_id"])
    elif "customer_id" in df.columns:
        df = df.dropna(subset=["customer_id"])
    elif "total_amount" in df.columns:
        df = df.dropna(subset=["total_amount"])

    # print(f"Recuento de valores nulos por cada columna (DESPUES DE LIMPIAR):\n")
    # print(df.isnull().sum())

    return df

# ============================================================================================================
def eliminar_repetidos(df):
    print(f"Recuendo de valores repetidos por columna ANTES: {df.duplicated().sum()}\n")
    
    # Este método no funciona porque la función list( no tiene el atributo "duplicated")
    # list(dict.fromkeys(df))

    if "order_date" in df.columns:
        df = df.sort_values("order_date").drop_duplicates(
            subset = ["order_id"],
            keep = "last")
    else:
        df = df.drop_duplicates()

    print(f"Recuendo de valores repetidos por columna DESPUES: {df.duplicated().sum()}\n")

    return df

# ============================================================================================================
def corregir_data_type(df):
    # Para esto usé df.info() para ver el tipo de datos de cada columna y evaluar si era correcto. Por ejemplo, había muchas fechas declaradas como string
    # Fui tomando nota de las columnas a modificar para poder crear un condicional de las columnas a corregir.
    # Luego con print(df.head()) miré algunos ejemplos para corroborar lo anterior.
    # Uso el método .fillna(0) para aquellas celdas que contienen NaN (y que decidí no eliminar en una función anterior)
    
    # Convertir a formato date, las fechas encontradas como strings
    for columna in columnas_de_fechas:
        if columna in df.columns:
            df[columna] = df[columna].fillna(0)
            df[columna] = pd.to_datetime(df[columna], format = 'mixed')
    
    # Convertir a integer, los años declados como float64
    for columna in columnas_de_integer:
        if columna in df.columns:
            df[columna] = df[columna].fillna(0).astype(int)

    # Convertir a boolean, los campos que sólo necesitan True/False o 1/0
    for columna in columnas_de_boolean:
        if columna in df.columns:
            df[columna] = df[columna].fillna(0).astype(bool)

    # Verificacion
    # df.info()
    # print(df.head())

    return df

# ============================================================================================================

# Metodo 1: bucle FOR porque perfmite más control en un ETL real
# Método 2: list comprehension para mayor brevedad (pero la lógica no escala en un ETL grande)
# data = [pd.read_csv(file) for file in csv_files]

# Creo diccionario para almacenar cada dataset procesado y diferenciado por nombre.
datasets = {}

for file in csv_files:
    df = pd.read_csv(file)

    # Obtener nombre de cada dataset para poder referenciarlos luego 
    nombre_dataset = os.path.splitext(os.path.basename(file))[0]

    # Otra forma de extraer tanto el nombre como la extensión es
    # nombre, extension = os.path.splitext(os.path.basename(file))
    # De esta forma se obtiene una tupla y se puede llamar por el campo, no por un indice

    mostrar_datos(df)
    df= eliminar_nulos(df)
    df = eliminar_repetidos(df)
    df = corregir_data_type(df)
    datasets[nombre_dataset] = df
    # print(nombre_dataset)

# Los nombres que se imprimen en la terminal son los nombres de los archivos, es decir:
# ecommerce_brands, ecommerce_categories, ecommerce_customers, ecommerce_inventory, ecommerce_orders,
# ecommerce_order_items, ecommerce_products, ecommerce_promotions, ecommerce_reviews, ecommerce_suppliers,
# ecommerce_warehouses

# ============================================================================================================
# Paso 7) RESPONDER PREGUNTAS DE NEGOCIO

# Pregunta 1) ¿Cuáles son los 5 clientes que más gastaron?

# Luego de revisar los DF con print(df.head()) vemos que:
# a) El campo "customer_id" aparece en "ecommerce_customers" y en "ecommerce_orders" 
# b) podemos unir (merge) ambos para poder consultar nombre de cliente y monto total gastado

df_customer_orders = pd.merge(datasets["ecommerce_customers"], datasets["ecommerce_orders"], on="customer_id", how="left")

# Metodo 1: mantiene la tabla original y agrega una nueva
# df_customer_orders["total_gastado"] = df_customer_orders.groupby(["first_name", "last_name"])["total_amount"].transform('sum')

# Metodo 2: construye una tabla nueva con las columnas del groupy() y agrega una nueva luego del agg())
df_customer_orders = df_customer_orders.groupby(["customer_id"], as_index=False).agg(
    total_gastado = ("total_amount", 'sum'),
    cantidad_ordenes = ("order_id", 'count')
)

df_customer_orders = df_customer_orders.sort_values('total_gastado', ascending=False)
df_top_five_customers = df_customer_orders.head()
print(f"*** Los 5 clientes que más gastaron fueron: ***")
print(f"{df_top_five_customers}\n")

# ============================================================================================================
# Pregunta 2) ¿Cuál es el producto más vendido (por cantidad)?

# a) El campo "product_id" aparece en "ecommerce_products" y en "ecommerce_order_items" 
# b) En ese último también aparece "quantity" así que podemos unirlos (merge) para sumar las cantidades en base al "product_id"

df_products_order_items = pd.merge(datasets["ecommerce_products"], datasets["ecommerce_order_items"], on="product_id", how="left")

# Agrupamos por "product_id" y "productname" para luego sumar el campo "quantity"
df_products_order_items = df_products_order_items.groupby(["product_id", "product_name"], as_index=False).agg(
    cantidad_de_ventas = ("quantity", sum)
)
df_products_order_items = df_products_order_items.sort_values('cantidad_de_ventas', ascending=False)

df_producto_mas_vendido = df_products_order_items.head(1)

print(f"*** El producto más vendido fue: ***")
print(f"{df_producto_mas_vendido}\n")

# ============================================================================================================
# Pregunta 3) ¿Cómo evolucionaron las ventas mes a mes?

# a) El campo "order_date" y "total_amount" aparecen ambos en "ecomerce_orders"
# b) Me quedo con el campo "mes" obtenido de "order_date"

# Creo una copia en un DF separado. Si no agrego pd.DataFrame, el resultado no es un dataframe
df_orders = pd.DataFrame(datasets["ecommerce_orders"])

# Convierto la fecha del campo "order_date" para que sólo me deje el mes en un campo nuevo
df_orders["mes"] = datasets["ecommerce_orders"]["order_date"].dt.to_period("M")
df_ventas_mes = df_orders.groupby("mes")['total_amount'].sum().reset_index()

print(f"*** La evolución de ventas mes a mes fue: ***")
print(df_ventas_mes)

# ============================================================================================================
# Paso 8) Escribir resultados a CSV y a Parquet

# Crear carpeta de output si no existe
os.makedirs('output', exist_ok=True)

# Escribir a CSV
df_top_five_customers.to_csv(".\\output\\top_five_customers.csv", index=False)
df_producto_mas_vendido.to_csv(".\\output\\producto_mas_vendido.csv", index=False)
df_ventas_mes.to_csv(".\\output\\ventas_mes.csv", index=False)

# Escribir a Parquet
df_top_five_customers.to_parquet(".\\output\\top_five_customers.parquet", index=False)
df_producto_mas_vendido.to_parquet(".\\output\\producto_mas_vendido.parquet", index=False)
df_ventas_mes.to_parquet(".\\output\\ventas_mes.parquet", index=False)

# ============================================================================================================
# Paso 9) Comparar tamaños entre CSV y Parquet

cantidad_bytes_csv_01 = os.path.getsize('.\\output\\top_five_customers.csv')
cantidad_bytes_csv_02 = os.path.getsize('.\\output\\producto_mas_vendido.csv')
cantidad_bytes_csv_03 = os.path.getsize('.\\output\\ventas_mes.csv')

print(f"\n")
print(f"Cantidad de bytes del archivo 'top_five_customers.csv': {cantidad_bytes_csv_01}")
print(f"Cantidad de bytes del archivo 'producto_mas_vendido.csv': {cantidad_bytes_csv_02}")
print(f"Cantidad de bytes del archivo 'ventas_mes.csv': {cantidad_bytes_csv_03}")

cantidad_bytes_parquet_01 = os.path.getsize('.\\output\\top_five_customers.parquet')
cantidad_bytes_parquet_02 = os.path.getsize('.\\output\\producto_mas_vendido.parquet')
cantidad_bytes_parquet_03 = os.path.getsize('.\\output\\ventas_mes.parquet')

print(f"\n")
print(f"Cantidad de bytes del archivo 'top_five_customers.parquet': {cantidad_bytes_parquet_01}")
print(f"Cantidad de bytes del archivo 'producto_mas_vendido.parquet': {cantidad_bytes_parquet_02}")
print(f"Cantidad de bytes del archivo 'ventas_mes.parquet': {cantidad_bytes_parquet_03}")