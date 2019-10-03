"""
    Ce module est absolument incroyable
"""

import requests
from models import db, Client, Serie_disponible

# Page d'accueil
def accueil():
    url = "https://api.betaseries.com/shows/list"
    querystring = {"key":"7c2f686dfaad","v":"3.0","limit":"1"}
    result = requests.request("GET", url, params=querystring)
    return result


# tri des series par genre
def serie_par_genre():
    url = "https://api.betaseries.com/shows/genres"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "limit": "2"}
    result = requests.request("GET", url, params=querystring)
    return result

# tri des series par date
# def serie_par_date():
#     url = "https://api.betaseries.com/shows/list"
#     querystring = {"key": "7c2f686dfaad", "v": "3.0", "limit": "2", "recent":True}
#     result = requests.request("GET", url, params=querystring)
#     return result # Pas trivial

# tri des series par ordre alphabetique
# def serie_par_alphabet():
#     url = "https://api.betaseries.com/shows/list"
#     querystring = {"key": "7c2f686dfaad", "v": "3.0", "limit": "2", "order":"alphabetical"}
#     result = requests.request("GET", url, params=querystring)
#     return result # Pas trivial


# fiche synoptique d'une serie avec ses saisons et episodes
def fiche_serie(id):
    url = "https://api.betaseries.com/shows/episodes"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "id":id}
    result = requests.request("GET", url, params=querystring)
    url2 = "https://api.betaseries.com/shows/seasons"
    result2 = requests.request("GET", url2, params=querystring)
    url3 = "https://api.betaseries.com/shows/display"
    result3 = requests.request("GET", url3, params=querystring)
    return result, result2, result3

# rechercher une serie par un nom
def recherche_serie(title):
    url = "https://api.betaseries.com/shows/search"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "nbpp": "10", "title":title}
    result = requests.request("GET", url, params=querystring)
    return result


# inscription a la base utilisateur
def inscription_base(adresse, mdp, user):
    db.session.add(Client(adresse, mdp, user))
    db.session.commit()

# connection a la base utilisateur
def connection_base():
    pass

# affichage de la liste de serie preferee
def serie_préférée():
    pass

# ajout a la liste de serie préférée
def ajout_préférée():
    pass

# notification serie preferee et recente
def notification():
    pass

