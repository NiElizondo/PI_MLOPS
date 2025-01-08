# Sistema de Recomendación de Películas - MVP

**Descripción:**

Este proyecto implementa un sistema de recomendación de películas como MVP (Minimum Viable Product) para una start-up que ofrece servicios de agregación de plataformas de streaming. 

El proyecto aborda la necesidad de procesar datos de películas, construir un modelo de recomendación y desplegar una API para acceder a las funcionalidades del sistema.


## Descripción del Problema

La start-up necesita un sistema de recomendación de películas, pero los datos disponibles presentan desafíos como:

* Datos anidados.
* Valores nulos.
* Falta de automatización en la actualización de datos.

Este proyecto busca construir un MVP que solucione estos problemas y permita a la empresa comenzar a utilizar el sistema de recomendación.

## Transformaciones de Datos

Se realizaron las siguientes transformaciones en los datos:

* **Desanidado de campos:** `belongs_to_collection`, `production_companies`, etc.
* **Imputación de valores nulos:**  `revenue` y `budget` rellenados con 0.
* **Eliminación de filas:** Filas con valores nulos en `release_date`.
* **Formato de fecha:**  `release_date` en formato AAAA-mm-dd.
* **Creación de columna:** `release_year` con el año de estreno.
* **Creación de columna:** `return` con el retorno de inversión (`revenue` / `budget`).
* **Eliminación de columnas:** `video`, `imdb_id`, `adult`, `original_title`, `poster_path` y `homepage`.

## API

Se desarrolló una API utilizando FastAPI con los siguientes endpoints:

* **`/cantidad_filmaciones_mes/{mes}`:** 
    * Devuelve la cantidad de películas estrenadas en un mes dado.
    * **Parámetro:** `mes` (str): Mes en español (e.g., "enero", "febrero").
    * **Respuesta:**  JSON con la cantidad de películas y un mensaje informativo.
    * **Ejemplo:** `/cantidad_filmaciones_mes/marzo`

* **`/cantidad_filmaciones_dia/{dia}`:**
    * Devuelve la cantidad de películas estrenadas en un día de la semana dado.
    * **Parámetro:** `dia` (str): Día de la semana en español (e.g., "lunes", "martes").
    * **Respuesta:** JSON con la cantidad de películas y un mensaje informativo.
    * **Ejemplo:** `/cantidad_filmaciones_dia/viernes`

* **`/score_titulo/{titulo}`:**
    * Devuelve el título, año de estreno y score de una película.
    * **Parámetro:** `titulo` (str): Título de la película.
    * **Respuesta:** JSON con el título, año de estreno y score de la película, o un mensaje de error si la película no se encuentra.
    * **Ejemplo:** `/score_titulo/The Shawshank Redemption`

* **`/votos_titulo/{titulo}`:**
    * Devuelve el título, cantidad de votos y promedio de votaciones de una película.
    * **Parámetro:** `titulo` (str): Título de la película.
    * **Respuesta:** JSON con el título, cantidad de votos y promedio de votaciones de la película, o un mensaje de error si la película no se encuentra o no tiene suficientes votos.
    * **Ejemplo:** `/votos_titulo/Inception`


* **`/recomendacion/{titulo}`:**
    * Devuelve una lista de 5 películas similares a la ingresada.
    * **Parámetro:** `titulo` (str): Título de la película.
    * **Respuesta:** JSON con una lista de 5 títulos de películas similares.
    * **Ejemplo:** `/recomendacion/Toy Story` 

## Análisis Exploratorio de Datos (EDA)

Se realizó un análisis exploratorio de los datos para identificar relaciones entre variables, outliers y patrones. Se incluyeron visualizaciones como nubes de palabras para analizar la frecuencia de palabras en los títulos de las películas.

## Sistema de Recomendación

Se implementó un sistema de recomendación basado en la similitud de puntuación entre películas. El sistema utiliza TF-IDF para vectorizar los títulos de las películas y cosine similarity para calcular la similitud entre ellas.

## Deployment

La API se desplegó utilizando Render.

## Tecnologías Utilizadas

* Python
* Pandas
* Scikit-learn
* FastAPI
* Render (o el servicio de deployment que hayas elegido)
* TfidfVectorizer
* cosine_similarity

## Resultados

* Se logró construir un MVP funcional con un sistema de recomendación de películas.
* La API permite acceder a la información y funcionalidades del sistema.
* El EDA proporcionó insights sobre los datos.

## Futuras Mejoras

* Implementar un sistema de recomendación más sofisticado.
* Automatizar la actualización de datos.
* Mejorar el rendimiento de la API.
* Añadir más funcionalidades a la API.
