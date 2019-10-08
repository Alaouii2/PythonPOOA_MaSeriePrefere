"""
    Ce module est absolument incroyable
"""
from models import db
import smtplib
import requests
from models import db, Client, Liste_serie_preferee
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    liste = Client.query.get()
    if user not in liste.user and adresse not in liste.adresse:
        db.session.add(Client(adresse, mdp, user))
        db.session.commit()
        return "Inscription complétée"
    else:
        return "Ce compte existe déjà"

connected = False

# connection a la base utilisateur
def connection_base(mdp, adresse):
    liste = Client.query.get()
    if (mdp, adresse) in (liste.user, liste.adresse):
        connected = True
    else:
        return "Désolé, mauvaise adresse ou mot de passe"

# affichage de la liste de serie preferee
def serie_préférée(adresse):
    series = Liste_serie_preferee.query.get(adresse)
    return series

# ajout a la liste de serie préférée
def ajout_préférée(serie, adresse):
    series = Liste_serie_preferee.query.get(adresse)
    db.session.add(Liste_serie_preferee(adresse, series))
    db.session.commit()
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

    message = 'Ces episodes de vos series favorites vont bientot etre diffuses :\n\n'
    for notification in liste:
        message = message + notification['show_title'] + ' (episode ' + str(notification['episode_number']) + ') : le ' + \
               notification['air_date'].strftime('%d/%m/%Y')

    msg = MIMEMultipart()
    msg['From'] = 'XXX@gmail.com'
    msg['To'] = 'YYY@gmail.com'
    msg['Subject'] = 'Tes series préférées'

    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login('XXX@gmail.com', 'PASSWORD')
    mailserver.sendmail('XXX@gmail.com', 'XXX@gmail.com', msg.as_string())
    mailserver.quit()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 500)
    server.ehlo()
    server.login('ouraorphe@gmail.com','55555555')
