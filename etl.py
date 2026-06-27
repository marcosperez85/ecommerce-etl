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
    print(f"*** Informacion de {os.path.basename(file)} ***\n")
    print(f"Cantidad de filas: {len(df)}, cantidad de columnas: {len(df.columns)}\n")
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
            df[columna] = pd.to_datetime(df[columna], format = 'mixed').dt.date
    
    # Convertir a integer, los años declados como float64
    for columna in columnas_de_integer:
        if columna in df.columns:
            df[columna] = df[columna].fillna(0).astype(int)

    # Convertir a boolean, los campos que sólo necesitan True/False o 1/0
    for columna in columnas_de_boolean:
        if columna in df.columns:
            df[columna] = df[columna].fillna(0).astype(bool)

    # Verificacion
    df.info()
    print(df.head())    
    
# ============================================================================================================
# Mostrar info de cada archivo dentro del array
# No uso range(0,10) en zip() para no hardcodear la cantidad de archivos

# Metodo 1: bucle FOR porque perfmite más control en un ETL real
# Método 2: list comprehension para mayor brevedad (pero la lógica no escala en un ETL grande)
# data = [pd.read_csv(file) for file in csv_files]

for file in csv_files:
    df = pd.read_csv(file)
    mostrar_datos(df)
    eliminar_nulos(df)
    eliminar_repetidos(df)
    corregir_data_type(df)