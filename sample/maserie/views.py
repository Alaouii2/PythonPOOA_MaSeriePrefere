"""
    Mesdames et messieurs, veuillez vous lever pour views !
    C'est le module gérant le front de notre application
"""

from flask import Flask, render_template
import requests

# Crée l'application Flask
app = Flask(__name__)

# Charge les options de configuration
app.config.from_object('config')

#Classe de requete
class Requete():
    pass

# Routage des pages

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

# @app.route('/contents/<int:content_id>/')
# def content(content_id):
#     return '%s' % content_id
