"""
    Ce module est absolument incroyable
"""
from models import db
import smtplib
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
    client = db.session.query('Client')
    for Client in client:
        Liste_Notif=[]
        Liste_préférée = serie_préférée(Client)
        for serie in Liste_préférée:
            prochaine_episode= serie.nextEpisode() #fonction à définir
        if prochaine_episode is None:
            continue
        Liste_Notif.append(prochaine_episode)

        if len(Liste_Notif) > 0:
            envoi_email(Client.email,Liste_Notif)
def envoi_email(mail,liste):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 500)
    server.ehlo()
    server.login('ouraorphe@gmail.com','55555555')






    pass







    pass
