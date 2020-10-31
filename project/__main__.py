from Functions_FA import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import time
import pandas as pd
import numpy as np
import sys
sys.setrecursionlimit(5000)

genres_dict = { 'AC': 'Acción', 'AN': 'Animación', 'AV': 'Aventuras', 'C-F': 'Ciencia ficción',
                'DR': 'Drama', 'FAN': 'Fantástico', 'INF': 'Infantil', 'INT': 'Intriga',
                'TE': 'Terror','WE': 'Western', 'CO': 'Comedia', 'DO': 'Documental', 'RO': 'Romance',
                'TH': 'Thriller', 'WE': 'Western'}
base_url = "https://www.filmaffinity.com/es/advsearch.php?page=%s&stype[]=title&genre=%s&fromyear=%s&toyear=%s"

def descarga_filmaffinity(year_1, year_2):
    '''Downloads all characteristicos for each movie beteeen two years
    both included, then treats and returns dataframe with all of them'''
    titles = []
    countries = []
    years = []
    genres = []
    direction = []
    casting = []
    marks = []
    continuation_response = True
    for y in range(year_1, year_2+1):
        time.sleep(600)
        for g in genres_dict.keys():
            continuation_pages = True
            for p in range(1,16):
                if continuation_response == True and continuation_pages == True:
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
                        soup = BeautifulSoup(page.content, 'html.parser')
                        if len(movie_titles(soup)) < 20:
                            continuation_pages = False
                            break
                        else:
                            titles = titles + movie_titles(soup)
                            countries = countries + movie_countries(soup)
                            years = years + [y for t in movie_titles(soup)]
                            genres = genres + [genres_dict.get(g) for t in movie_titles(soup)]
                            direction = direction + movie_direction(soup)
                            casting = casting + movie_casting(soup)
                            marks = marks + movie_marks(soup)
    df = pd.DataFrame(list(zip(titles, countries, years, genres, direction, casting, marks)), 
               columns =['Título', 'País', 'Año', 'Género', 'Dirección', 'Reparto', 'Nota']) 
    df["Dirección"] = df["Dirección"].str.join(', ')
    df["Reparto"] = df["Reparto"].str.join(', ')
    temp_title=df.Título
    temp_genre=df.Género
    df['Tipo filme'] = pd.np.where(temp_title.str.contains(' \(C\)'),"Cortometraje",
                        pd.np.where(temp_title.str.contains("\(TV\)"), "Estreno televisivo",
                        pd.np.where(temp_title.str.contains("\(Serie de TV\)"), "Serie",
                        pd.np.where(temp_genre.str.contains("Documental"), "Documental",
                        pd.np.where(temp_title.str.contains("\(Miniserie de TV\)"), "Miniserie", "Película")))))

    df_final = df.groupby(['Título', 'Año', 'País', 'Dirección', 'Reparto', 'Nota','Tipo filme'])                        ['Género'].apply(list).to_frame().reset_index()
    df_final["Género"] = df_final["Género"].str.join(', ')
    df_final = df_final[df_final['Título'].notna()]
    return df_final
    
if __name__ == '__main__':
    result = descarga_filmaffinity(1900, 2020)