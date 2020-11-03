# Se importan las librerías requeridas, incluyendo las propias de Functions_FA
from Functions_FA import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import time
import pandas as pd
import numpy as np
import sys
# El límite de recursión debe ser incrementado
sys.setrecursionlimit(5000)

# Este diccionario propio engloba los géneros admitidos en el buscador avanzado de Filmaffinity
genres_dict = { 'AC': 'Acción', 'AN': 'Animación', 'AV': 'Aventuras', 'C-F': 'Ciencia ficción',
                'DR': 'Drama', 'FAN': 'Fantástico', 'INF': 'Infantil', 'INT': 'Intriga',
                'TE': 'Terror','WE': 'Western', 'CO': 'Comedia', 'DO': 'Documental', 'RO': 'Romance',
                'TH': 'Thriller', 'WE': 'Western'}

# Esta URL a completar relativa al buscador avanzado de Filmaffinity será transformada a lo largo de varias iteraciones
base_url = "https://www.filmaffinity.com/es/advsearch.php?page=%s&stype[]=title&genre=%s&fromyear=%s&toyear=%s"

def descarga_filmaffinity(year_1, year_2):
    '''Downloads all characteristicos for each movie beteeen two years
    both included, then treats and returns dataframe with all of them'''
#Declaramos listas vacías para los campos de interés
    titles = []
    countries = []
    years = []
    genres = []
    direction = []
    casting = []
    marks = []
    continuation_response = True
    for y in range(year_1, year_2+1):
        # Sin este tiempo de consulta de 10 minutos para sets de x años Filmaffinity expulsa a la URL peticionaria.
        # El tamaño de dichos sets puede ser de 20 años (principios de s. XX) o de 3 (finales década de 2010) debido
        # al alto número de títulos en este último periodo en contraposición al anterior.
        time.sleep(600)
        for g in genres_dict.keys():
            # Esta variable decide cuándo es posible dejar de consultar páginas posteriores por cada búsqueda
            continuation_pages = True
            for p in range(1,16):
                if continuation_response == True and continuation_pages == True:
                    # Este tiempo de espera evita hacer demasiadas peticiones por minuto
                    time.sleep(0.25)
                    url = base_url % (p, g, y, y)
                    page = requests.get(url)
                    if str(page) == "<Response [429]>":
                        print("kicked out")
                        continuation_response = False
                        break
                    elif str(page) != "<Response [200]>":
                        continuation_pages = False
                        break
                    else:
                        # Se crea la "sopa" con el contenido en html a parsear
                        soup = BeautifulSoup(page.content, 'html.parser')
                        if len(movie_titles(soup)) < 20:
                             # En el momento que sea identificada la última página de la consulta,
                             #cambiamos la variable continuation_pages para evitar consultas innecesarias
                            continuation_pages = False
                            break
                        else:
                            # Agregamos los elementos extraidos por las funciones a las listas.
                            titles = titles + movie_titles(soup)
                            countries = countries + movie_countries(soup)
                            years = years + [y for t in movie_titles(soup)]
                            genres = genres + [genres_dict.get(g) for t in movie_titles(soup)]
                            direction = direction + movie_direction(soup)
                            casting = casting + movie_casting(soup)
                            marks = marks + movie_marks(soup)
    # Creamos un dataframe a partir de las listas vacías previamente creadas
    df = pd.DataFrame(list(zip(titles, countries, years, genres, direction, casting, marks)), 
               columns =['Título', 'País', 'Año', 'Género', 'Dirección', 'Reparto', 'Nota']) 
    # Para el caso de Dirección y Reparto al contener una sublista, hacemos join de sus valores
    df["Dirección"] = df["Dirección"].str.join(', ')
    df["Reparto"] = df["Reparto"].str.join(', ')
    #creamos dos listas temporales con el fin de extraer los campos de Título y Genero, a partir
    # de ellas vamos a definir un nuevo atributo llamado Tipo Filme 
    temp_title=df.Título
    temp_genre=df.Género
    df['Tipo filme'] = pd.np.where(temp_title.str.contains(' \(C\)'),"Cortometraje",
                        pd.np.where(temp_title.str.contains("\(TV\)"), "Estreno televisivo",
                        pd.np.where(temp_title.str.contains("\(Serie de TV\)"), "Serie",
                        pd.np.where(temp_genre.str.contains("Documental"), "Documental",
                        pd.np.where(temp_title.str.contains("\(Miniserie de TV\)"), "Miniserie", "Película")))))
    # Con este groupby fusionamos títulos con varios géneros en una sola línea que engloba todos esos géneros
    df_final = df.groupby(['Título', 'Año', 'País', 'Dirección', 'Reparto', 'Nota','Tipo filme'])                        ['Género'].apply(list).to_frame().reset_index()
    df_final["Género"] = df_final["Género"].str.join(', ')
    df_final = df_final[df_final['Título'].notna()]
    return df_final
    
if __name__ == '__main__':
    result = descarga_filmaffinity(1900, 2020)