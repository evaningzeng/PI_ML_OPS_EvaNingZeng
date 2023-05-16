import pandas as pd
import numpy as np
import json
from ast import literal_eval

# Función para convertir la columna 'popularity' a tipo float
def convert_popularity(value):
    try:
        return float(value)
    except ValueError:
        return float('nan')

# Función para evaluar de forma segura una cadena de texto como un objeto de Python
def safe_literal_eval(value):
    try:
        return literal_eval(value)
    except (ValueError, SyntaxError):
        return None

# Función para obtener el nombre del primer país de producción
def get_country_name(country_str):
    try:
        country_list = json.loads(country_str.replace("'", "\""))
        if len(country_list) > 0:
            return country_list[0]['name']
    except (json.JSONDecodeError, TypeError):
        pass
    return None

# Función para procesar la columna 'production_countries'
def process_countries(data):
    # Convertir la columna a tipo string
    data['production_countries'] = data['production_countries'].astype(str)
    # Rellenar los valores nulos con una cadena vacía
    data['production_countries'] = data['production_countries'].fillna(value='')
    # Obtener el nombre del primer país de producción
    data['country'] = data['production_countries'].apply(get_country_name)
    # Eliminar la columna original
    return data.drop(columns=['production_countries'])

# Función para procesar la columna 'belongs_to_collection'
def process_collection(data):
    # Evaluar de forma segura la columna como un objeto de Python
    data['belongs_to_collection'] = data['belongs_to_collection'].apply(lambda x: safe_literal_eval(x) if pd.notna(x) else x)
    # Extraer las columnas 'collection_id' y 'collection_name'
    data['collection_id'] = data['belongs_to_collection'].apply(lambda x: x['id'] if isinstance(x, dict) and 'id' in x else None)
    data['collection_name'] = data['belongs_to_collection'].apply(lambda x: x['name'] if isinstance(x, dict) and 'name' in x else None)
    return data

# Función para procesar la columna 'production_companies'
def process_companies(data):
    # Evaluar de forma segura la columna como un objeto de Python
    data['production_companies'] = data['production_companies'].apply(lambda x: safe_literal_eval(x) if pd.notna(x) else x)
    # Extraer las columnas 'companies_id' y 'companies_name'
    data['companies_id'] = data['production_companies'].apply(lambda x: [comp['id'] for comp in x] if isinstance(x, list) else [])
    data['companies_name'] = data['production_companies'].apply(lambda x: [comp['name'] for comp in x] if isinstance(x, list) else [])
    return data

# Función para procesar las columnas 'revenue' y 'budget'
def process_revenue_budget(data):
    # Convertir las columnas a valores numéricos y rellenar los valores nulos con 0
    data['revenue'] = pd.to_numeric(data['revenue'], errors='coerce').fillna(0)
    data['budget'] = pd.to_numeric(data['budget'], errors='coerce').fillna(0)
    return data

# Función para procesar la columna 'release_date'
def process_dates(data):
    # Eliminar las filas con valores nulos
    data.dropna(subset=['release_date'], inplace=True)
    # Convertir la columna a tipo datetime y extraer el año de lanzamiento en una nueva columna
    data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    data['release_year'] = pd.to_datetime(data['release_date'], errors='coerce').dt.year
    data['release_year'] = data['release_year'].fillna(0).astype(int)
    return data

# Función para calcular el retorno de inversión
def calculate_return(data):
    # Calcular el retorno de inversión y almacenarlo en una nueva columna
    data['return'] = data['revenue'] / data['budget']
    data['return'] = data['return'].fillna(0)
    return data

# Función para eliminar las columnas que no serán utilizadas
def drop_unneeded_columns(data):
    columns_to_drop = ['video', 'imdb_id', 'adult', 'original_title', 'vote_count', 'poster_path', 'homepage']
    return data.drop(columns=columns_to_drop)

# Función principal
def main():
    # Definir el conversor para la columna 'popularity'
    converters = {"popularity": convert_popularity}
    # Leer el archivo CSV
    data = pd.read_csv("https://storage.googleapis.com/pimlopsenz/dataset/movies_dataset.csv", converters=converters)
    # Aplicar las transformaciones
    data = process_countries(data)
    data = process_collection(data)
    data = process_companies(data)
    data = process_revenue_budget(data)
    data = process_dates(data)
    data = calculate_return(data)
    data = drop_unneeded_columns(data)
    # Guardar el DataFrame resultante en un nuevo archivo CSV
    data.to_csv('dataset/processed_movies_dataset.csv', index=False)
    # Imprimir mensaje de finalización
    print("Transformaciones completadas. El archivo 'processed_movies_dataset.csv' ha sido guardado.")


if __name__ == "__main__":
    main()