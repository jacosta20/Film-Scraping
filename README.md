# Film Scramping

La industria del entretenimiento audiovisual no para de crecer, acorde al Theme Report del 2019  de emitido por Motion Picture association, para el 2019 representó un mercado de 100 billones de dólares. Con el crecimiento de la industria, se sobre entiende que existe un constante crecimiento de la oferta y la demanda, lo que quiere decir que anualmente existen cientos de películas disponibles (según el reporte 835 para el 2019, casi 100 más comparado con el año anterior). Son muchas personas a quienes les gusta disfrutar de una gran película, sin embargo, en los tiempos actuales, en los cuales el tiempo es un bien preciado.
Acorde al reporte, las personas entre 25 y 39 años representan la mayor población que asiste al cine, con un promedio de 4.2 asistencias por año al cine por persona. Lo que representa que cada persona que asiste ocasionalmente al cine espera seleccionar la película correcta, aquella película que cumpla con sus gustos. Existen páginas de críticas de cine con calificaciones y revisiones, sin embargo, puede tomar tiempo hasta que muchas personas hagan su aporte para aquellos que se guían de la calificación.
Por eso será de utilidad obtener un data set con películas que contenga información que necesitamos para poder predecir gustos basados en apreciaciones anteriores, títulos, géneros, directores, efectos visuales, calificaciones, etc. 
En este sentido, hemos identificado una página web que nos puede ayudar a cumplir este cometido, pretendemos hacer scraping de esta página con el fin de tratar sus datos y poder realizar diferentes análisis posteriores:
https://www.filmaffinity.com/es/advsearch.php?page=2&stype[]=title&genre=AV&fromyear=1992&toyear=1992

Identificación del archivo Robots.txt
A partir de la identificación del archivo ubicado en https://www.filmaffinity.com/robots.txt, obtenemos los siguientes resultados:

User-agent: *
Disallow: /*?FASID
Disallow: /*&FASID
Disallow: /*/sharerating
Disallow: /flash/rats.swf

pip install python-whois

import whois 

print(whois.whois('https://www.filmaffinity.com/'))

