import requests
import streamlit as st

# URL de tu backend FastAPI en render.com
BASE_URL = "https://pi-ml-ops-evaningzeng.onrender.com"

# Función para realizar la solicitud al endpoint de recomendación
def obtener_recomendacion(titulo):
    url = f"{BASE_URL}/recomendacion/{titulo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("recomendaciones", [])
    return []

# Interfaz de usuario con Streamlit
def main():
    st.title("Sistema de Recomendación de Películas")

    # Formulario para ingresar el título de la película
    titulo = st.text_input("Ingrese el título de la película")

    # Botón para obtener las recomendaciones
    if st.button("Obtener Recomendaciones"):
        if titulo:
            recomendaciones = obtener_recomendacion(titulo)
            if recomendaciones:
                st.subheader("Recomendaciones:")
                for i, recomendacion in enumerate(recomendaciones):
                    st.write(f"{i+1}. {recomendacion}")
            else:
                st.write("No se encontraron recomendaciones.")
        else:
            st.write("Ingrese el título de la película.")

if __name__ == "__main__":
    main()
