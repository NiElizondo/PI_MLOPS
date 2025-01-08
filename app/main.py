import pandas as pd
from fastapi import FastAPI
from modelo import crear_modelo_recomendacion, obtener_recomendaciones

app = FastAPI()

# Diccionarios de meses y días
meses = {
    "enero": "January",
    "febrero": "February",
    "marzo": "March",
    "abril": "April",
    "mayo": "May",
    "junio": "June",
    "julio": "July",
    "agosto": "August",
    "septiembre": "September",
    "octubre": "October",
    "noviembre": "November",
    "diciembre": "December"
}

dias_semana = {
    "lunes": "Monday",
    "martes": "Tuesday",
    "miercoles": "Wednesday",
    "jueves": "Thursday",
    "viernes": "Friday",
    "sabado": "Saturday",
    "domingo": "Sunday"
}

# Cargar dataset limpio
df = pd.read_csv("movies_dataset_clean.csv")

# Convertir la columna release_date a datetime
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Cargar dataset limpio y reducirlo a 1000 filas
df_reduc = df.head(1000) # <-- Para seleccionar las primeras 1000 filas

# Crear el modelo de recomendación con el dataset reducido
vectorizer, tfidf_matrix, cosine_sim = crear_modelo_recomendacion(df_reduc)


@app.get("/")
def home():
    """
    Endpoint principal de la API.
    """
    return {"mensaje": "API funcionando correctamente. Visita /docs para más detalles."}


def obtener_pelicula(titulo: str):
    """
    Obtiene la fila del DataFrame correspondiente a la película con el título dado.
    """
    pelicula = df[df['title'].str.lower() == titulo.lower()]
    if pelicula.empty:
        return None
    return pelicula.iloc[0]


@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    """
    Devuelve la cantidad de películas estrenadas en un mes dado.
    """
    try:
        # Validar que el mes ingresado sea válido
        if mes.lower() not in meses:
            return {"error": f"El mes '{mes}' no es válido. Usa un mes como 'enero', 'febrero', etc."}

        # Obtener el mes en inglés
        mes_ingles = meses[mes.lower()]

        # Crear una nueva columna con el mes de lanzamiento
        df['month'] = df['release_date'].dt.month_name()

        # Contar las películas estrenadas en el mes especificado
        cantidad = df[df['month'] == mes_ingles].shape[0]

        # Crear el mensaje de salida
        mensaje = f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}."

        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    """
    Devuelve la cantidad de películas estrenadas en un día de la semana dado.
    """
    try:
        # Validar que el día ingresado sea válido
        if dia.lower() not in dias_semana:
            return {"error": f"El día '{dia}' no es válido. Usa un día como 'lunes', 'martes', etc."}

        # Obtener el día en inglés
        dia_ingles = dias_semana[dia.lower()]

        # Crear una nueva columna con el día de la semana
        df['day_of_week'] = df['release_date'].dt.day_name()

        # Contar las películas estrenadas en el día especificado
        cantidad = df[df['day_of_week'] == dia_ingles].shape[0]

        # Crear el mensaje de salida
        mensaje = f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}."

        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    """
    Devuelve el título, año de estreno y score de una película.
    """
    try:
        pelicula = obtener_pelicula(titulo)
        if pelicula is None:
            return {"error": f"La película '{titulo}' no fue encontrada."}

        # Obtener los valores necesarios
        fecha_lanzamiento = pelicula['release_date']
        puntaje = pelicula['vote_average']

        # Validar que 'release_date' no sea nulo
        if pd.isna(fecha_lanzamiento):
            return {"error": f"La película '{titulo}' no tiene registrada una fecha de estreno."}

        # Convertir la fecha al año
        anio = fecha_lanzamiento.year

        # Crear el mensaje de salida
        mensaje = f"La película '{titulo}' fue estrenada en el año {anio} con un score/popularidad de {puntaje}."

        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    """
    Devuelve el título, cantidad de votos y promedio de votaciones de una película.
    """
    try:
        pelicula = obtener_pelicula(titulo)
        if pelicula is None:
            return {"error": f"La película '{titulo}' no fue encontrada."}

        # Obtener los valores necesarios
        fecha_lanzamiento = pelicula['release_date']
        total_votos = pelicula['vote_count']
        promedio_votos = pelicula['vote_average']

        # Validar que 'release_date' no sea nulo
        if pd.isna(fecha_lanzamiento):
            return {"error": f"La película '{titulo}' no tiene registrada una fecha de estreno."}

        # Convertir la fecha al año
        anio = fecha_lanzamiento.year

        # Validar que el total de votos sea mayor a 2000
        if total_votos < 2000:
            return {"mensaje": f"La película '{titulo}' no cumple con el requisito de contar con al menos 2000 valoraciones."}

        # Crear el mensaje de salida
        mensaje = f"La película '{titulo}' fue estrenada en el año {anio}. La misma cuenta con un total de {total_votos} valoraciones, con un promedio de {promedio_votos}."

        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


# Función de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    """
    Devuelve una lista de películas similares a la ingresada.
    """
    try:
        # Obtener recomendaciones
        peliculas_similares = obtener_recomendaciones(titulo, df_reduc, cosine_sim)

        if peliculas_similares:
            return {
                "mensaje": f"Películas similares a '{titulo}':",
                "recomendaciones": peliculas_similares,
            }
        else:
            return {"error": f"No se encontraron películas similares a '{titulo}'"}

    except Exception as e:
        # Manejar errores no esperados
        return {"error": f"Se produjo un error: {str(e)}"}