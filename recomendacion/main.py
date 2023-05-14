from pydantic import BaseModel
from fastapi import FastAPI
import pandas as pd
import uvicorn
from model import create_tfidf_model

# Creamos la aplicación
app = FastAPI()

# Cargar los datos
df = pd.read_csv('https://storage.googleapis.com/pimlopsenz/dataset/processed_movies_dataset.csv')

# Cargar el modelo TF-IDF y la matriz de similitud
tfidf, cosine_sim, indices = create_tfidf_model(df)

class Movie(BaseModel):
    title: str

# Mensaje inicial de saludos
@app.get("/")
def read_root():
    return {"message": "Hola, bienvenido a nuestra API de películas!"}

# Endpoint para recomendación de películas
@app.get("/recomendacion/")
def get_recommendations(title: str):
    # Obtener el índice de la película que coincide con el título
    idx = indices[title]

    # Obtener las puntuaciones de similitud de todas las películas con esa película
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas en función de las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener las puntuaciones de las 10 películas más similares
    sim_scores = sim_scores[1:6]

    # Obtener los índices de películas
    movie_indices = [i[0] for i in sim_scores]

    # Devolver las cinco películas más similares
    return {'lista recomendada': df['title'].iloc[movie_indices].tolist()}

# Iniciamos la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
