"""
    Mesdames et messieurs, veuillez vous lever pour views !
    C'est le module gérant le front de notre application
"""

from flask import Flask, render_template , request , session , redirect ,url_for
import requests
import hashlib, uuid,os
import sqlite3
conn = sqlite3.connect('app.db')
cursor=conn.cursor()
# Crée l'application Flask
app = Flask(__name__)

# Charge les options de configuration
app.config.from_object('config')

#Classe de requete
class Requete():
    pass

# Routage des pages

## from .utils import find_content, OpenGraphImage

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

@app.route('/my_list/')
def my_list():
    url = "https://api.betaseries.com/shows/random"
    querystring = {"key":"7c2f686dfaad","v":"3.0","nb":"3"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    return render_template('my_list.html', posts=posts)

@app.route('/series_alphabet/')
def series_alphabet():
    url = "https://api.betaseries.com/shows/random"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "nb": "9"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    return render_template('series_alphabet.html', posts=posts)

@app.route('/series_categories/')
def series_categories():
    return render_template('series_categories.html')

@app.route('/serie/')
def serie():
    url = "https://api.betaseries.com/shows/episodes"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "id":1993}
    episodes = requests.request("GET", url, params=querystring).json()
    url2 = "https://api.betaseries.com/shows/seasons"
    saisons = requests.request("GET", url2, params=querystring).json()
    url3 = "https://api.betaseries.com/shows/display"
    display = requests.request("GET", url3, params=querystring).json()
    return render_template('serie.html', episodes=episodes, saisons=saisons, display=display)

@app.route('/about/')
def about():
    return render_template('about.html')


@app.route("/register/", methods=["GET", "POST"])
def register():

    error = None

    if "e_mail" in session:
        return redirect(url_for('se connecter'))

    if request.method == "GET":
        return render_template("register.html",)
    if request.method == "POST":

        id_client= str(uuid.uuid4())
        nom_utilisateur = request.form["Nom d'utilisateur"]
        adresse_mail = request.form["Email"]
        mdp = request.form["Password"]
        mdp2= request.form["Repeat Password"]
        mdp_hash = hashlib.sha256(str(mdp).encode("utf-8")).hexdigest()


        """verifier si l'e-mail n'est pas deja utilisé par un client"""

        req_client_existant = "SELECT * FROM main.client WHERE adresse_mail = '%s' "
        cursor.execute(req_client_existant % adresse_mail)
        resultat_req_client_existant = cursor.fetchall()
        print(resultat_req_client_existant)


        '''Si on a déjà un e-mail avec cette adresse, on dit que le mail est déjà utilisé'''

        if len(resultat_req_client_existant) > 0:
            error = 'Cette adresse courriel est deja utilisee, veuillez utiliser une autre adresse'
            return render_template("enregistrer_client.html",error = error)

        #"""Sinon on enregistre les informations du client dans la BD"""

        else:

            req_enregister_client = "INSERT INTO main.client (id_client,adresse_mail,mdp,nom_utilisateur)VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(req_enregister_client,(id_client,adresse_mail,mdp,nom_utilisateur))
            conn.commit()

            return redirect(url_for('home'))





# @app.route('/contents/<int:content_id>/')
# def content(content_id):
#     return '%s' % content_id
