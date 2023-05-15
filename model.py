import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Suponemos que df es el DataFrame cargado
df = pd.read_csv('https://storage.googleapis.com/pimlopsenz/dataset/processed_movies_dataset.csv')

# Crear el vectorizador TF-IDF y transformar los títulos de las películas
tfidf = TfidfVectorizer(stop_words='english')
df['title'] = df['title'].fillna('')
tfidf_matrix = tfidf.fit_transform(df['title'])

# Calcular la matriz de similitud
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Crear un mapeo inverso de índices y títulos de películas
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def recomendacion(title, cosine_sim=cosine_sim):
    # Obtener el índice de la película que coincide con el título
    idx = indices[title]

    # Obtener las puntuaciones de similitud de todas las películas con esta película
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas en función de las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener las puntuaciones de las 5 películas más similares
    sim_scores = sim_scores[1:6]

    # Obtener los índices de las películas
    movie_indices = [i[0] for i in sim_scores]

    # Devolver los cinco títulos más similares
    return df['title'].iloc[movie_indices].tolist()
