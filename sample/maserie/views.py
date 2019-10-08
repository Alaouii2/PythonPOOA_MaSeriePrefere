"""
    Mesdames et messieurs, veuillez vous lever pour views !
    C'est le module gérant le front de notre application
"""

from flask import Flask, render_template , request , session , redirect ,url_for
import requests
import hashlib, uuid,os
# Crée l'application Flask
app = Flask(__name__)

# Charge les options de configuration
app.config.from_object('config')

#Classe de requete
class Requete():
    pass

# Routage des pages

## from .utils import find_content, OpenGraphImage

@app.route('/')
@app.route('/home/')
def home():
    url = "https://api.betaseries.com/shows/list"
    querystring = {"key":"7c2f686dfaad","v":"3.0","limit":"3"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    return render_template('home.html', posts=posts)

@app.route('/series/')
def series():
    return render_template('series.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/game-single/')
def gamesingle():
    return render_template('game-single.html')

@app.route('/register/')
def register():
    return render_template('register.html')


@app.route("/enregistrer_client", methods=["GET", "POST"])
def enregistrer_client():

    error = None

    if "e_mail" in session:
        return redirect(url_for('se connecter'))

    if request.method == "GET":
        return render_template("register.html",)
    if request.method == "POST":

        id_client= str(uuid.uuid4())
        adresse_mail = request.form["Email"]
        mdp = request.form["Password"]
        mdp2= request.form["Repeat Password"]
        mdp_hash = hashlib.sha256(str(mdp).encode("utf-8")).hexdigest()


        """verifier si l'e-mail n'est pas deja utilisé par un client"""

        req_client_existant = "SELECT * FROM main.client WHERE adresse_mail = '%s' "
        cursor.execute(req_client_existant % e_mail)
        resultat_req_client_existant = cursor.fetchall()
        print(resultat_req_client_existant)


        '''Si on a déjà un e-mail avec cette adresse, on dit que le mail est déjà utilisé'''

        if len(resultat_req_client_existant) > 0:
            error = 'Cette adresse courriel est deja utilisee, veuillez utiliser une autre adresse'
            return render_template("enregistrer_client.html",error = error)

        #"""Sinon on enregistre les informations du client dans la BD"""

        else:

            req_enregister_client = "INSERT INTO main.client (id_client,adresse_mail,mdp)VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(req_enregister_client,(id_client,adresse_mail,mdp))
            connection.commit()

            session["e_mail"] = request.form["e_mail"]

            """Inserer image par defaut"""

            requete_inserer_image = "INSERT INTO Image (IdImage, Nom, IdClient) VALUES ('%s','%s','%s')"
            id_image = str(uuid.uuid4())
            nom = "default.jpg"
            cursor.execute(requete_inserer_image % (id_image, nom, id_client))
            connection.commit()


            return redirect(url_for('mes_informations'))





# @app.route('/contents/<int:content_id>/')
# def content(content_id):
#     return '%s' % content_id
