import pandas as pd
import glob
import os

lista_df = []

path = "c:\\Marcos\\Programacion\\ecommerce-etl-python\\data"
lista_archivos = os.listdir(path)
ruta_archivos = glob.glob(os.path.join(path, '*.csv'))

lista_df = [pd.read_csv(archivo) for archivo in ruta_archivos]

# print(lista_df[0].duplicated().sum())

for elem,count in zip(lista_df, range(0,10)):
    print(f"*****Informacion de {lista_archivos[count]}*****\n")
    print(elem.head())
    print(elem.info())
    print(elem.describe())

    print("\nVisualizar elementos nulos\n")
    print(elem.isnull().sum())

    print(f"\nCantidad de elementos repetidos: {elem.duplicated().sum()}\n")

    # Luego de correr el script vemos que:
    # 1) Cantidad de campos nulos en
    #   a) ecommerce_categories para el campo "parent_category_id" por un total de 7
    #   b) ecommerce_orders para los campos
    #       promotion_id:   765
    #       notes:          837
    #   Para el caso de notes, no es importante dado que son notas
    #   
    #
    # 2) No hay valores repetidos en ninguno de los datasets



