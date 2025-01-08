import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def crear_modelo_recomendacion(df):
    """
    Crea un modelo de recomendación basado en la similitud del título de las películas.

    Args:
        df (pd.DataFrame): DataFrame con los datos de las películas, incluyendo la columna 'title'.

    Returns:
        tuple: Una tupla que contiene el vectorizador TF-IDF, la matriz TF-IDF 
               y la matriz de similitud coseno.
    """
    try:
        # Vectorizar títulos
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(df['title'].fillna(''))

        # Calcular similitudes
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

        return vectorizer, tfidf_matrix, cosine_sim
    except Exception as e:
        print(f"Error al crear el modelo de recomendación: {e}")
        return None, None, None


def obtener_recomendaciones(titulo, df, cosine_sim):
    """
    Obtiene recomendaciones de películas similares a la película dada.

    Args:
        titulo (str): Título de la película.
        df (pd.DataFrame): DataFrame con los datos de las películas.
        cosine_sim (np.array): Matriz de similitud coseno.

    Returns:
        list: Lista de títulos de películas similares.
    """
    try:
        # Buscar el índice de la película en el DataFrame
        idx = df[df['title'].str.contains(titulo, case=False, na=False)].index
        if len(idx) == 0:
            return []  # Retornar una lista vacía si no se encuentra la película

        # Obtener el índice de la primera coincidencia
        idx = idx[0]

        # Calcular los puntajes de similitud
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:6]  # Excluir la película misma

        # Extraer las películas similares
        peliculas_similares = [df.iloc[i[0]]['title'] for i in sim_scores]
        return peliculas_similares

    except Exception as e:
        print(f"Error al obtener recomendaciones: {e}")
        return []