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

{
  "domain_name": [
    "FILMAFFINITY.COM",
    "filmaffinity.com"
  ],
  "registrar": "Arsys Internet, S.L. dba NICLINE.COM",
  "whois_server": "whois.nicline.com",
  "referral_url": null,
  "updated_date": [
    "2020-06-21 07:21:16",
    "2015-01-13 15:24:07"
  ],
  "creation_date": "2001-06-20 14:23:27",
  "expiration_date": "2021-06-20 14:23:27",
  "name_servers": [
    "NS1.FILMAFFINITY.COM",
    "NS2.FILMAFFINITY.COM"
  ],
  "status": [
    "ok https://icann.org/epp#ok",
    "ok https://www.icann.org/epp#ok"
  ],
  "emails": [
    "email@nicline.com",
    "whoiscontact@domainconnection.info"
  ],
  "dnssec": [
    "unsigned",
    "Unsigned"
  ],
  "name": "REDACTED FOR PRIVACY",
  "org": null,
  "address": "REDACTED FOR PRIVACY",
  "city": "REDACTED FOR PRIVACY",
  "state": "Madrid",
  "zipcode": "REDACTED FOR PRIVACY",
  "country": "ES"
}
