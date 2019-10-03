"""
    Ce module est absolument incroyable
"""

import requests

url = "https://api.betaseries.com/shows/list"

# Page d'accueil
def accueil():
    querystring = {"key":"7c2f686dfaad","v":"3.0","limit":"1"}
    result = requests.request("GET", url, params=querystring)
    return result


response = accueil()
print(response.json())

# tri des series par genre
def serie_par_genre():
    pass

# tri des series par date
def serie_par_date():
    pass

# tri des series par ordre alphabetique
def serie_par_alphabet():
    pass

# affichage de la liste de serie preferee
def serie_préférée():
    pass

# fiche synoptique d'une serie avec ses saisons et episodes
def fiche_serie():
    pass

# connection a la base utilisateur
def connection_base():
    pass

# inscription a la base utilisateur
def inscription_base():
    pass

# notification serie preferee et recente
def notification():
    pass
