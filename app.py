import requests
import streamlit as st
from urllib.parse import quote


# Define la URL del punto de acceso de la API
API_URL = "http://localhost:8000"

# Define las rutas de los puntos de acceso
RECOMMENDATION_PATH = "/recomendacion/"

# Define la aplicación de Streamlit
def app():
    # Establece el título de la aplicación
    st.title("Aplicación de Recomendación de Películas")

    # Obtén la entrada del usuario
    title = st.text_input("Ingresa el título de una película")

    # Realiza la solicitud a la API
    if title:
        response = requests.get(API_URL + RECOMMENDATION_PATH + quote(title))
        if response.status_code == 200:
            recommended_movies = response.json()["lista recomendada"]
            st.write("Películas recomendadas:")
            for movie in recommended_movies:
                st.write("- " + movie)
        else:
            st.write("Error: " + str(response.status_code))

# Ejecuta la aplicación
if __name__ == "__main__":
    app()
