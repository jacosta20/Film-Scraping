#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote
import time
import pandas as pd
import numpy as np

def movie_titles(soup):
    '''Returns a list with the titles of the movies 
    from the filmaffinity advance search html'''
    names_div = soup.findAll('div', {'class':'mc-title'})
    movie_titles(soup)

    titles=[]
    for n in names_div:
        titles.append(str(n)[str(n).find('title="')+len('title="'):str(n).rfind('">')])
    return titles

def movie_countries(soup):
    '''Returns a list with the countries the movies come
    from at the filmaffinity advance search html'''
    countries_div = soup.findAll('div', {'class':'mc-title'})
    countries=[]
    for n in countries_div:
        country_string = str(n)[-30:]
        countries.append(country_string[country_string.find('title="')+len('title="'):country_string.rfind('"/></div>')])
    return countries

def movie_marks(soup):
    '''Returns a list with the marks given to the movies
    read at the filmaffinity advance search html'''
    marks_div = soup.findAll('div', {'class':'avgrat-box'})
    marks=[]
    for m in marks_div:
        marks.append(str(m)[str(m).find('"avgrat-box">')+len('"avgrat-box">'):str(m).rfind("</div>")])
    return marks

def movie_direction(soup):
    '''Returns a list with the director(s) names from to the 
    movies read at the filmaffinity advance search html'''
    direction_div = soup.findAll('div', {'class':'mc-director'})
    direction = []
    for c in direction_div:
        number_directors = str(c).count("type=director")
        directors_list = []
        for i in str(c).split('type=director', number_directors):
            director_name = i[i.find(";stext=")+len(";stext="):i.rfind('" title=')]
            if "%20" in director_name:
                director_name = unquote(director_name.replace("=", "%"))
                directors_list.append(director_name)
        direction.append(directors_list)
    return direction


def movie_casting(soup):
    '''Returns a list with the casting names(s) from to the 
    movies read at the filmaffinity advance search html'''
    casting_div = soup.findAll('div', {'class':'mc-cast'})
    casting = []
    for c in casting_div:
        number_actors = str(c).count("type=cast")
        actors_list = []
        for i in str(c).split('type=cast', number_actors):
            actor_name = i[i.find(";stext=")+len(";stext="):i.rfind('" title=')]
            if "%20" in actor_name:
                actor_name = unquote(actor_name.replace("=", "%"))
                actors_list.append(actor_name)
        casting.append(actors_list)
    return casting


def descarga_filmaffinity(year_1, year_2):
    '''Downloads all characteristicos for each movie beteeen two years
    both included, then treats and returns dataframe with all of them'''
    import time
    titles = []
    countries = []
    years = []
    genres = []
    direction = []
    casting = []
    marks = []
    continuation_response = True
    for y in range(year_1, year_2+1):
        print(1)
        time.sleep(360)
        for g in genres_dict.keys():
            continuation_pages = True
            for p in range(1,16):
                if continuation_response == True and continuation_pages == True:
                    time.sleep(0.25)
                    url = base_url % (p, g, y, y)
                    # print(url)
                    page = requests.get(url)
                    # print(page)
                    if str(page) == "<Response [429]>":
                        print("kicked out")
                        continuation_response = False
                        break
                    elif str(page) != "<Response [200]>":
                        # print("bad response, skipping pages")
                        continuation_pages = False
                        break
                    else:
                        soup = BeautifulSoup(page.content, 'html.parser')
                        # print(movie_titles(soup))
                        if len(movie_titles(soup)) < 20:
                            # print("not going to page 2")
                            continuation_pages = False
                            break
                        else:
                            titles = titles + movie_titles(soup)
                            countries = countries + movie_countries(soup)
                            # countries = countries + [counties_dict.get(c) for t in movie_titles(soup)]
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

    df_final = df.groupby(['Título', 'Año', 'País', 'Dirección', 'Reparto', 'Nota','Tipo filme'])                ['Género'].apply(list).to_frame().reset_index()
    df_final["Género"] = df_final["Género"].str.join(', ')
    df_final = df_final[df_final['Título'].notna()]
    return df_final

