"""
    Mesdames et messieurs, veuillez vous lever pour views !
    C'est le module gérant le front de notre application
"""

from flask import Flask, render_template, request, session, redirect, url_for
import requests
import hashlib, uuid, os
import sqlite3

#Crée une connection à la base de donnée
conn = sqlite3.connect('app.db', check_same_thread=False)
cursor = conn.cursor()

# Crée l'application Flask
app = Flask(__name__)

# Charge les options de configuration
app.config.from_object('config')

#Classe de requete
class Requete():
    pass

# Routage des pages

# La page d'accueil. Affiche trois séries au hasard.
@app.route('/')
@app.route('/home/')
def home():
    url = "https://api.betaseries.com/shows/random"
    querystring = {"key":"7c2f686dfaad","v":"3.0","nb":"3"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    for post in posts:
        if len(post["description"]) > 500:
            post["description"] = post["description"][:500] + "..."
    return render_template('home.html', posts=posts)

@app.route('/series/<starting>/<int:page>/')
def series(starting, page):
    url = "https://api.betaseries.com/shows/list"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "order": "alphabetical", "limit": "9", "starting": starting,
                   "start": (page-1)*9, "fields": "id,title,images.show"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    for post in posts:
        if len(post.keys()) == 2:
            post['images'] = {'show': url_for('static', filename='img/logo.png')}
    return render_template('series.html', posts=posts, starting=starting, page=page)

@app.route('/serie/<int:serie_id>/')
def serie(serie_id):
    url = "https://api.betaseries.com/shows/episodes"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "id":serie_id}
    episodes = requests.request("GET", url, params=querystring).json()["episodes"]
    url2 = "https://api.betaseries.com/shows/seasons"
    saisons = requests.request("GET", url2, params=querystring).json()["seasons"]
    url3 = "https://api.betaseries.com/shows/display"
    display = requests.request("GET", url3, params=querystring).json()["show"]
    return render_template('serie.html', episodes=episodes, saisons=saisons, display=display)

@app.route('/my_list/')
def my_list():
    url = "https://api.betaseries.com/shows/random"
    querystring = {"key":"7c2f686dfaad","v":"3.0","nb":"3"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    return render_template('my_list.html', posts=posts)

@app.route("/register/", methods=["GET", "POST"])
def register():
    error = None

    if "e_mail" in session:
        return redirect(url_for('se connecter'))

    if request.method == "GET":
        return render_template("register.html", )
    if request.method == "POST":

        id_client = str(uuid.uuid4())
        nom_utilisateur = request.form["username"]
        adresse_mail = request.form["email"]
        mdp = request.form["psw"]
        mdp2 = request.form["psw-repeat"]

        # """verifier si l'e-mail n'est pas deja utilisé par un client"""

        req_client_existant = "SELECT * FROM main.client WHERE adresse_mail = ?"
        cursor.execute(req_client_existant, (adresse_mail,))
        resultat_req_client_existant = cursor.fetchall()
        print(resultat_req_client_existant)

        # '''Si on a déjà un e-mail avec cette adresse, on dit que le mail est déjà utilisé'''

        if len(resultat_req_client_existant) > 0:
            error = 'Cette adresse courriel est deja utilisée, veuillez utiliser une autre adresse'
            return (render_template("register.html", error=error))

        # """Sinon on enregistre les informations du client dans la BD"""

        elif (mdp != mdp2):
            error = "Vous devez utiliser le même mot de passe"
            return (render_template("register.html", error=error))

        else:
            cursor.execute("INSERT INTO client(id_client, adresse_mail, mdp, nom_utilisateur) VALUES(?,?,?,?);",(id_client, adresse_mail, mdp, nom_utilisateur))
            conn.commit()
            return (redirect(url_for('home')))

