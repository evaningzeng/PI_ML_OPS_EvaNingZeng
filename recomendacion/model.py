import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def create_tfidf_model(df):
    # Crear un vectorizer TF-IDF
    tfidf = TfidfVectorizer(stop_words='english')

    # Llenar los NaN con una cadena vacía
    df['overview'] = df['overview'].fillna('')

    # Construir la matriz TF-IDF
    tfidf_matrix = tfidf.fit_transform(df['overview'])

    # Calcular la similitud de coseno
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Crear un mapeo inverso de índices y títulos de películas
    indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    return tfidf, cosine_sim, indices
