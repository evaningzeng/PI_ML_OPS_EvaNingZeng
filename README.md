# Proyecto Individual Nº1: Machine Learning Operations (MLOps)

En este proyecto, se desarrollará un sistema de recomendación de películas para una start-up de agregación de plataformas de streaming 🎬🚀.

Como `Data Scientist` en el rol de `MLOps Engineer`, el objetivo es implementar un modelo de `Machine Learning` para recomendación de películas en un entorno de producción. Se trabajará en un `MVP` (*Minimum Viable Product*) para la start-up, con el desafío de tenerlo listo en una semana 🛠⏰.

Los datos iniciales presentan limitaciones en calidad y estructura. Por lo tanto, se realizará un trabajo de `Data Engineering` para transformarlos y prepararlos adecuadamente. El proyecto se centrará en llevar el modelo desde su etapa inicial hasta la implementación en producción, brindando información valiosa y mejoras según los resultados y necesidades de la empresa. 💡📊 

La propuesta de trabajo incluye las siguientes etapas:

## Transformaciones de datos:

Ver código en Transformaciones/transformaciones.py

Se realizaron transformaciones específicas en los datos para limpiarlos y prepararlos para su posterior procesamiento.

1. Los campos anidados como 'belongs_to_collection', 'production_companies' fueron desanidados para extraer información relevante:
   - Para 'belongs_to_collection': Se extrajeron las columnas 'collection_id' y 'collection_name' del campo anidado.
   - Para 'production_companies': Se extrajeron las columnas 'companies_id' y 'companies_name' del campo anidado.
2. Los valores nulos en los campos 'revenue' y 'budget' fueron rellenados con el número 0.
3. Los valores nulos en el campo 'release_date' fueron eliminados.
4. Las fechas en el campo 'release_date' fueron formateadas al formato AAAA-mm-dd y se creó una nueva columna llamada 'release_year' para extraer el año de la fecha de estreno.
5. Se creó una columna llamada 'return' que calcula el retorno de inversión dividiendo los campos 'revenue' y 'budget'. En caso de que no haya datos disponibles para calcularlo, se asigna el valor 0.
6. Se eliminaron las columnas que no serán utilizadas en el análisis, incluyendo 'video', 'imdb_id', 'adult', 'original_title', 'vote_count', 'poster_path' y 'homepage'.

En resumen, las transformaciones realizadas se enfocaron en desanidar campos anidados, rellenar valores nulos, formatear fechas, calcular el retorno de inversión y eliminar columnas innecesarias. Estas transformaciones permiten tener un conjunto de datos más limpio y preparado para análisis posteriores.

## Desarrollo de una API

Ver código en App/main.py

Se utilizó el framework FastAPI para desarrollar una API que permita acceder a los datos de la empresa. Se implementaron 6 funciones para diferentes endpoints, que brindan información sobre películas estrenadas en un mes o día específico, franquicias de películas, películas producidas en un país, productoras de películas y el retorno de inversión de una película en particular.

## Deployment

Link: [https://pi-ml-ops-evaningzeng.onrender.com](https://pi-ml-ops-evaningzeng.onrender.com/)

Se utilizó el servicio de Render para desplegar la API y permitir su consumo desde la web. Probar el funcionamiento de la API en https://pi-ml-ops-evaningzeng.onrender.com/docs. Escribe los parámetros en minúscula. 

## Análisis exploratorio de los datos: (Exploratory Data Analysis-EDA)

Ver en eda.ipynb

Se realizó un análisis exploratorio de los datos para comprender las relaciones entre las variables, identificar outliers o anomalías, y descubrir patrones interesantes que puedan ser útiles en análisis posteriores. Se utilizaron herramientas como pandas profiling, missingno para generar reportes y obtener conclusiones. El EDA incluye gráficas interesantes para extraer datos, como por ejemplo una nube de palabras con las palabras más frecuentes en los títulos de las películas.

## Sistema de recomendación

Ver el código en Modelo/model.py

Probar el API en https://pi-ml-ops-evaningzeng.onrender.com/docs#/default/obtener_recomendacion_recomendacion__titulo__get

Link de interface gráfico: https://evaningzeng-pi-ml-ops-evaningzeng-app-4ckgp9.streamlit.app/

Se implementó un sistema de recomendación de películas basado en el modelo Nearest Neighbors utilizando TF-IDF. La función `recomendacion` toma un título de película como entrada y devuelve una lista de las 5 películas más similares en orden descendente de similitud. El modelo se ajusta a los datos de películas seleccionados y limpios y utiliza la métrica del coseno para medir la similitud.

Esta funcionalidad adicional se agregó a la API anteriormente desarrollada.

Debido a las limitaciones de memoria RAM del servicio de Render, se implementó una solución más simple y eficiente en lugar de una más precisa y compleja para el sistema de recomendación de películas. Aunque esta solución puede no ser tan precisa, sigue siendo efectiva y adecuada para el entorno con recursos limitados.

## Video Demo

Link:

Se hizo un video para mostrar el funcionamiento de la API y los resultados del modelo de machine learning entrenado.