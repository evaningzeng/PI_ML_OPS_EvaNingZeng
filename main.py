from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd
import uvicorn
from model import recomendacion

# Cargamos los datos
df = pd.read_csv('https://storage.googleapis.com/pimlopsenz/dataset/processed_movies_dataset.csv')

df['release_date'] = pd.to_datetime(df['release_date'])  # Convertir a datetime
df['month'] = df['release_date'].dt.month_name(locale='es')  # Extraer el nombre del mes en español
df['day'] = df['release_date'].dt.day_name(locale='es')  # Extraer el nombre del mes en español

# Creamos la aplicación
app = FastAPI()

class Movie(BaseModel):
    title: str


# Mensaje inicial de saludos
@app.get("/")
def read_root():
    return {"message": "Hola, bienvenido a nuestra API de películas!"}

# Endpoint para obtener la cantidad de películas por mes
@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes: str):
    try:
        count = df[df['month'] == mes.capitalize()].shape[0]
        return {'mes':mes, 'cantidad':count}
    except Exception as e:
        print(f"Error: {e}")

# Endpoint para obtener la cantidad de películas por día
@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia: str):
    try:
        count = df[df['day'] == dia.capitalize()].shape[0]
        return {'dia':dia, 'cantidad':count}
    except Exception as e:
        print(f"Error: {e}")

# Endpoint para obtener información de una franquicia
@app.get("/franquicia/{franquicia}")
def franquicia(franquicia: str):
    subset = df[df['title'] == franquicia]
    pertenece_a_franquicia = not pd.isnull(subset['collection_name'].values[0])

    if pertenece_a_franquicia:
        franquicia = subset['collection_name'].values[0]
        franquicia_subset = df[df['collection_name'] == franquicia]
        cantidad = len(franquicia_subset)
        ganancia_total = franquicia_subset['revenue'].sum()
        ganancia_promedio = franquicia_subset['revenue'].mean()

        return {
            'franquicia': franquicia,
            'cantidad': cantidad,
            'ganancia_total': ganancia_total,
            'ganancia_promedio': ganancia_promedio
        }
    else:
        return {'mensaje': f"La franquicia '{franquicia}' no existe."}

# Endpoint para obtener la cantidad de películas por país
@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais: str):
    try:
        count = df[df['country'] == pais].shape[0]
        return {'pais':pais, 'cantidad':count}
    except Exception as e:
        print(f"Error: {e}")

# Endpoint para obtener información de una productora
@app.get("/productoras/{productora}")
def productoras(productora: str):
    try:
        subset = df[df['production_companies'].str.contains(productora, na=False)]
        total_revenue = subset['revenue'].sum()
        count = subset.shape[0]
        return {'productora':productora, 'ganancia_total':total_revenue, 'cantidad':count}
    except Exception as e:
        print(f"Error: {e}")

# Endpoint para obtener información de una película
@app.get("/retorno/{pelicula}")
def retorno(pelicula: str):
    try:
        subset = df.loc[df['title'] == pelicula, ['budget', 'revenue', 'return', 'release_year']]
        if subset.empty:
            return {'error': f"The movie '{pelicula}' does not exist in the DataFrame."}

        info_pelicula = subset.iloc[0].to_dict()
        info_pelicula['pelicula'] = pelicula
        info_pelicula['release_year'] = int(info_pelicula['release_year'])

        return {
            'pelicula': info_pelicula['pelicula'],
            'inversion': info_pelicula['budget'],
            'ganancia': info_pelicula['revenue'],
            'retorno': info_pelicula['return'],
            'anio': info_pelicula['release_year']
        }

    except Exception as e:
        print(f"Error: {e}")

# Endpoint para recomendación de películas
@app.get("/recomendacion/{titulo}")
async def obtener_recomendacion(titulo: str):
    lista_recomendada = recomendacion(titulo)
    return {'lista recomendada': lista_recomendada}


# Iniciamos la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
