from flask import render_template, flash, redirect, url_for, request
import requests
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Liste_series
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import sqlite3
from ast import literal_eval


# indiquer quand fait une fois (Add devient Supp)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
    """
    Route menant au menu d'accueil
    """
    # L'utilisateur identifié peut ajouter une nouvelle série à sa liste
    if request.method == 'POST':
        l = literal_eval(request.form.get('button'))
        ajout(l)
        return (""), 204
    # Page d'accueil, affiche 3 séries au hasard
    url = "https://api.betaseries.com/shows/random"
    querystring = {"key": "7c2f686dfaad", "v": "3.0", "nb": "3"}
    posts = requests.request("GET", url, params=querystring).json()["shows"]
    for post in posts:
        if len(post["description"]) > 500:
            post["description"] = post["description"][:500] + "..."
    bonjour = ""

    # Si l'utilisateur est authentifié, affiche son nom dans le message de bienvenue
    if current_user.is_authenticated:
        bonjour = current_user.username
    return render_template('home.html', posts=posts, bonjour=bonjour)


@app.route('/series/', methods=['GET', 'POST'])
def series():
    """
    Route menant à la liste de séries disponibles
    """
    # Affiche la liste des séries suivant la lettre et l'index choisits
    if request.method == 'GET':
        url = "https://api.betaseries.com/shows/list"
        starting = request.args.get('starting', default=' ', type=str)
        page = request.args.get('page', default=1, type=int)
        querystring = {"key": "7c2f686dfaad", "v": "3.0", "order": "alphabetical", "limit": "9", "starting": starting,
                       "start": (page - 1) * 9, "fields": "id,title,images.show"}
        posts = requests.request("GET", url, params=querystring).json()["shows"]
        for post in posts:
            if len(post.keys()) == 2:
                post['images'] = {'show': url_for('static', filename='img/logo.png')}
            post['ajout'] = dans_maliste(post)
        return render_template('series.html', posts=posts, starting=starting, page=page)

    elif request.method == 'POST':
        # Affiche les résultat de recherche par nom, par appel à l'api
        if "search" in request.form:
            url = "https://api.betaseries.com/search/all"
            search = request.form['search']
            querystring = {"key": "7c2f686dfaad", "v": "3.0", "query": search, "limit": 100}
            posts = requests.request("GET", url, params=querystring).json()["shows"]
            for post in posts:
                images_url = "https://api.betaseries.com/shows/pictures"
                images = {"key": "7c2f686dfaad", "v": "3.0", "id": post["id"]}
                pictures_url = requests.request("GET", images_url, params=images).json()["pictures"]
                picture_url = [url for url in pictures_url if url['picked'] == 'show']
                post['images'] = {
                    'show': (picture_url[0]['url'] if picture_url else url_for('static', filename='img/logo.png'))}
                post['ajout'] = dans_maliste(post)
            return render_template('series.html', posts=posts, starting=None, page=None)

        # L'utilisateur identifié peut ajouter une nouvelle série à sa liste
        elif "button" in request.form:
            l = literal_eval(request.form.get('button'))
            ajout(l)
            return (""), 204

@app.route('/serie/', methods=["GET", "POST"])
def serie():
    """
    Route menant au descriptif d'une série
    """
    # L'utilisateur identifié peut ajouter une nouvelle série à sa liste
    if request.method == 'POST':
        l = literal_eval(request.form.get('button'))
        ajout(l)
        return (""), 204

    # Appelle l'api pour récupérer les informations pertinentes
    serie_id = request.args.get('serie_id', type=int)
    urls = ["https://api.betaseries.com/shows/episodes", "https://api.betaseries.com/shows/seasons",
            "https://api.betaseries.com/shows/display"]
    items = ["episodes", "seasons", "show"]
    requete_serie = Requete(serie_id, items, urls)
    response = requete_serie.run()
    return render_template('serie.html', serie_id=serie_id, episodes=response["episodes"], saisons=response["seasons"],
                           display=response["show"])


from threading import Thread, RLock
from queue import Queue


class Requete():
    """
    Cette classe permet d'effectuer des api call en parallèle
    """

    def __init__(self, serie_id, items, urls):
        self.querystring = {"key": "7c2f686dfaad", "v": "3.0", "id": serie_id}
        self.urls = urls
        self.items = items
        self.response = {}
        self.queue = Queue()
        self.verrou = RLock()
        for item in items:
            self.response[item] = ""

    # Crée et lance des thread en parallèle
    def run(self):
        self.queue.put(self.response)
        threads = [Thread(target=self.requete,
                          args=(self.querystring, item, self.verrou, self.queue, url))
                   for (item, url) in zip(self.items, self.urls)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.queue.get()

    # Un thread récupère les informations, et les stocke dans la réponse, gérée par un verrou
    @staticmethod
    def requete(querystring, item, verrou, queue, url):
        display = requests.request("GET", url, params=querystring).json()[item]
        with verrou:
            a = queue.get()
            a[item] = display
            queue.put(a)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route menant à la page d'identification
    """
    # Si l'utilisateur est déjà identifié, renvoie à la page d'accueil
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    # Sinon, récupère les données envoyées, les compare à la base de donnée
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Si les identifiants ne sont pas bons on redirige vers la page de connexion
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # On redirige vers la page appropriée une fois connecté : l'accueil si arrivé en tapant directement l'url, la page d'origine sinon
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """
    Route activant la déconnexion
    """
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Route menant à la page d'inscription
    """
    # Si l'utilisateur est déjà authentifié on retourne la page d'accueil
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    # Si le formulaire est correct on enregistre le nouvel utilisateur dans la base
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    """
    Route menant à la page utilisateur (A supprimer ?)
    """
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/my_list/', methods=['GET', 'POST'])
@login_required
def my_list():
    """
    Route menant à la page de la liste des séries préférées
    """
    if request.method == 'POST':
        print('post')
        serie_id = int(request.form.get('button'))
        print(serie_id)
        Liste_series.query.filter_by(serie_id=serie_id).delete()
        db.session.commit()
        return (""), 204
    liste = query_db('select * from liste_series where person_id = ? order by serie_name asc',
                     args=(current_user.get_id()))
    starting = request.args.get('starting', default=' ', type=str)
    page = request.args.get('page', default=1, type=int)
    return render_template('my_list.html', posts=liste, starting=starting, page=page)


from app.models import Notification
from flask import jsonify


@app.route('/notifications')
@login_required
def notifications():
    """
    Route activant le processus de rappatriement des nouvelles séries

    TODO : Ajd la fonction vérifie régulièrement le contenu des notifications pour prendre celles
    qui ont time stamp récent et qui n'ont pas encore été vues.
    Ce qu'on veut faire c'est call l'api de betaseries tout les jours à une heure définie
    (en fait non : si rajout d'une série, l'api call doit etre fait)
    (en fait on peut faire les deux : ca + dès qu'un rajout)
     pour prendre les séries des 8 prochains jours, mettre les nouvelles dans les notif
     puis les appeler et renvoyer les recentes non vues.

API call : https://api.betaseries.com/episodes/next?key=7c2f686dfaad&v=3.0&id=19
    """
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.payload_json,
        'timestamp': n.timestamp
    } for n in notifications])


from datetime import datetime


@app.route('/messages')
@login_required
def messages():
    """
    Route menant à la page de notifications
    """

    notifications = query_db('select * from Notification where timestamp > ? order by timestamp asc', args=(datetime(2012,10,10,10,10,10),))
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    return render_template('messages.html', messages=notifications)

# helpers

def query_db(query, args=(), one=False):
    """
    Fonction utilitaire pour appeler la base de donnée
    """
    dbase = sqlite3.connect('app.db')
    cur = dbase.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def ajout(l):
    s = [i[0] for i in query_db('select serie_id from liste_series where person_id=?', args=(current_user.get_id()))]
    serie_id = int(l[0])
    if serie_id not in s:
        serie_name = l[1]
        serie_pictureurl = l[2]
        serie = Liste_series(person_id=current_user.get_id(), serie_id=serie_id, serie_name=serie_name,
                             serie_pictureurl=serie_pictureurl)
        db.session.add(serie)
        db.session.commit()
    else:
        Liste_series.query.filter_by(serie_id=serie_id).delete()
        db.session.commit()


def dans_maliste(post):
    s = [i[0] for i in query_db('select serie_id from liste_series where person_id=?', args=(current_user.get_id()))]
    if post['id'] in s:
        return 'Enlever'
    else:
        return 'Ajouter'


