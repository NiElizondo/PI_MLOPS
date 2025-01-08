import pandas as pd
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente. Visita /docs para más detalles."}


# Cargar dataset limpio
df = pd.read_csv("movies_dataset_clean.csv")

# Convertir la columna release_date a datetime
df = pd.read_csv("movies_dataset_clean.csv", dtype={"column_name": str}, low_memory=False)


#Endpoint Cant Filmaciones/mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    try:
        # Diccionario para traducir los meses del año al inglés
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
        
        # Validar que el mes ingresado sea válido
        if mes.lower() not in meses:
            return {"error": f"El mes '{mes}' no es válido. Usa un mes como 'enero', 'febrero', etc."}
        
        # Obtener el mes en inglés
        mes_ingles = meses[mes.lower()]
        
        # Asegurar que la columna release_date sea tipo datetime
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        
        # Crear una nueva columna con el mes de lanzamiento
        df['month'] = df['release_date'].dt.month_name()
        
        # Contar las películas estrenadas en el mes especificado
        cantidad = df[df['month'] == mes_ingles].shape[0]
        
        # Crear el mensaje de salida
        mensaje = f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}."
        
        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


#Endpoint Cant filmaciones/dia
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    try:
        # Diccionario para traducir los días de la semana al inglés
        dias_semana = {
            "lunes": "Monday",
            "martes": "Tuesday",
            "miércoles": "Wednesday",
            "jueves": "Thursday",
            "viernes": "Friday",
            "sábado": "Saturday",
            "domingo": "Sunday"
        }
        
        # Validar que el día ingresado sea válido
        if dia.lower() not in dias_semana:
            return {"error": f"El día '{dia}' no es válido. Usa un día como 'lunes', 'martes', etc."}
        
        # Obtener el día en inglés
        dia_ingles = dias_semana[dia.lower()]
        
        # Asegurar que la columna release_date sea tipo datetime
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        
        # Crear una nueva columna con el día de la semana
        df['day_of_week'] = df['release_date'].dt.day_name()
        
        # Contar las películas estrenadas en el día especificado
        cantidad = df[df['day_of_week'] == dia_ingles].shape[0]
        
        # Crear el mensaje de salida
        mensaje = f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}."
        
        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


#Endpoint Score
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    try:
        # Filtrar el DataFrame por el título (insensible a mayúsculas/minúsculas)
        pelicula = df[df['title'].str.lower() == titulo.lower()]
        
        if pelicula.empty:
            return {"error": f"La película '{titulo}' no fue encontrada."}
        
        # Obtener los valores necesarios
        fecha_lanzamiento = pelicula.iloc[0]['release_date']
        puntaje = pelicula.iloc[0]['vote_average']
        
        # Validar que 'release_date' no sea nulo
        if pd.isna(fecha_lanzamiento):
            return {"error": f"La película '{titulo}' no tiene registrada una fecha de estreno."}

        # Convertir la fecha al año
        anio = pd.to_datetime(fecha_lanzamiento).year
        
        # Crear el mensaje de salida
        mensaje = f"La película '{titulo}' fue estrenada en el año {anio} con un score/popularidad de {puntaje}."
        
        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


#Endpoint Votos
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    try:
        # Filtrar el DataFrame por el título (insensible a mayúsculas/minúsculas)
        pelicula = df[df['title'].str.lower() == titulo.lower()]
        
        if pelicula.empty:
            return {"error": f"La película '{titulo}' no fue encontrada."}
        
        # Obtener los valores necesarios
        fecha_lanzamiento = pelicula.iloc[0]['release_date']
        total_votos = pelicula.iloc[0]['vote_count']
        promedio_votos = pelicula.iloc[0]['vote_average']
        
        # Validar que 'release_date' no sea nulo
        if pd.isna(fecha_lanzamiento):
            return {"error": f"La película '{titulo}' no tiene registrada una fecha de estreno."}

        # Convertir la fecha al año
        anio = pd.to_datetime(fecha_lanzamiento).year
        
        # Validar que el total de votos sea mayor a 2000
        if total_votos < 2000:
            return {"mensaje": f"La película '{titulo}' no cumple con el requisito de contar con al menos 2000 valoraciones."}
        
        # Crear el mensaje de salida
        mensaje = f"La película '{titulo}' fue estrenada en el año {anio}. La misma cuenta con un total de {total_votos} valoraciones, con un promedio de {promedio_votos}."
        
        return {"mensaje": mensaje}

    except Exception as e:
        return {"error": str(e)}


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Vectorizar títulos
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['title'].fillna(''))

# Calcular similitudes
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Función de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    try:
        # Verificar que el DataFrame 'df' y la matriz 'cosine_sim' estén definidos
        if df is None or cosine_sim is None:
            return {"error": "Los datos no están cargados correctamente"}

        # Buscar el índice de la película en el DataFrame
        idx = df[df['title'].str.contains(titulo, case=False, na=False)].index
        if len(idx) == 0:
            return {"error": f"La película '{titulo}' no fue encontrada en el dataset"}

        # Obtener el índice de la primera coincidencia
        idx = idx[0]

        # Verificar que el índice esté dentro del rango de la matriz cosine_sim
        if idx >= len(cosine_sim):
            return {"error": "Índice fuera de rango en la matriz de similitud"}

        # Calcular los puntajes de similitud
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]  # Excluir la película misma

        # Extraer las películas similares
        peliculas_similares = [df.iloc[i[0]]['title'] for i in sim_scores]
        return {
            "mensaje": f"Películas similares a '{titulo}':",
            "recomendaciones": peliculas_similares,
        }

    except Exception as e:
        # Manejar errores no esperados
        return {"error": f"Se produjo un error: {str(e)}"}


