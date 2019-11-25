from flask import render_template, flash, redirect, url_for, request
import requests
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Liste_series,Notification
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import sqlite3
from datetime import datetime
from ast import literal_eval
from flask_classful import FlaskView, route
from threading import Thread, RLock
from queue import Queue


class Requete:
    """
    Cette classe permet d'effectuer des api call en parallèle
    """

    def __init__(self, serie_ids, items, urls, names):
        self.serie_ids = serie_ids
        self.querystrings = [{"key": "7c2f686dfaad", "v": "3.0", "id": serie_id} for serie_id in serie_ids]
        self.urls = urls
        self.items = items
        self.response = {}
        self.queue = Queue()
        self.verrou = RLock()
        self.names = names
        for name in self.names:
            self.response[name] = ""

    # Crée et lance des thread en parallèle
    def run(self):
        self.queue.put(self.response)
        threads = [Thread(target=self.requete,
                          args=(querystring, item, self.verrou, self.queue, url, name))
                   for (querystring, item, url, name) in zip(self.querystrings, self.items, self.urls, self.names)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.queue.get()

    # Un thread récupère les informations, et les stocke dans la réponse, gérée par un verrou
    @staticmethod
    def requete(querystring, item, verrou, queue, url, name):
        try:
            display = requests.request("GET", url, params=querystring).json()[item]
        except:
            display = None
        with verrou:
            a = queue.get()
            a[name] = display
            queue.put(a)


class BaseView(FlaskView):

    def ajout(self, l):
        s = [i[0] for i in
             self.querydb('select serie_id from liste_series where person_id=?', args=(current_user.get_id(),))]
        serie_id = int(l[0])
        if serie_id not in s:
            serie_name = l[1]
            serie_pictureurl = l[2]
            serie = Liste_series(person_id=current_user.get_id(), serie_id=serie_id, serie_name=serie_name,
                                 serie_pictureurl=serie_pictureurl)
            db.session.add(serie)
            db.session.commit()
        else:
            Liste_series.query.filter_by(serie_id=serie_id, person_id=current_user.get_id()).delete()
            Notification.query.filter_by(serie_id=serie_id, user_id=current_user.get_id()).delete()
            db.session.commit()

    def dans_maliste(self, post):
        s = [i[0] for i in
             self.querydb(query='select serie_id from liste_series where person_id=?', args=(current_user.get_id(),))]
        if post['id'] in s:
            return 'Enlever'
        else:
            return 'Ajouter'

    def querydb(self, query, args=(), one=False):
        """
        Fonction utilitaire pour appeler la base de donnée
        """
        dbase = sqlite3.connect('app.db')
        cur = dbase.execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv


class SerieView(BaseView):
    @route('/', methods=["GET", "POST"])
    def serie(self):
        """
        Route menant au descriptif d'une série
        """
        # L'utilisateur identifié peut ajouter une nouvelle série à sa liste
        if request.method == 'POST':
            l = literal_eval(request.form.get('button'))
            self.ajout(l)
            return (""), 204

        # Appelle l'api pour récupérer les informations pertinentes
        serie_id = [request.args.get('serie_id', type=int) for i in range(3)]
        urls = ["https://api.betaseries.com/shows/episodes", "https://api.betaseries.com/shows/seasons",
                "https://api.betaseries.com/shows/display"]
        items = ["episodes", "seasons", "show"]
        requete_serie = Requete(serie_id, items, urls, items)
        response = requete_serie.run()
        ajouter = self.dans_maliste({'id': serie_id[0]})
        return render_template('serie.html', serie_id=serie_id[0], ajouter=ajouter, episodes=response["episodes"],
                               saisons=response["seasons"],
                               display=response["show"])


class SeriesView(BaseView):
    @route('/', methods=['GET', 'POST'])
    def series(self):
        """
        Route menant à la liste de séries disponibles
        """
        # Affiche la liste des séries suivant la lettre et l'index choisits
        if request.method == 'GET':
            url = "https://api.betaseries.com/shows/list"
            starting = request.args.get('starting', default=' ', type=str)
            page = request.args.get('page', default=1, type=int)
            querystring = {"key": "7c2f686dfaad", "v": "3.0", "order": "alphabetical", "limit": "9",
                           "starting": starting,
                           "start": (page - 1) * 9, "fields": "id,title,images.show"}
            posts = requests.request("GET", url, params=querystring).json()["shows"]
            for post in posts:
                if len(post.keys()) == 2:
                    post['images'] = {'show': url_for('static', filename='img/logo.png')}
                post['ajout'] = self.dans_maliste(post)
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
                    post['ajout'] = self.dans_maliste(post)
                return render_template('series.html', posts=posts, starting=None, page=None)

            # L'utilisateur identifié peut ajouter une nouvelle série à sa liste
            elif "button" in request.form:
                l = literal_eval(request.form.get('button'))
                self.ajout(l)
                return (""), 204


class NotificationsView(BaseView):

    decorators = [login_required]

    @route('/')
    @login_required
    def notifications(self):
        """
        Route activant le processus de rappatriement des nouvelles séries
        """

        # Récupère la liste de série préférée de l'utilisateur et effectue une requete api pour chaque série
        series = current_user.query.join(Liste_series).with_entities(Liste_series.serie_id).all()
        series = [series[index][0] for index in range(len(series))]
        urls = ["https://api.betaseries.com/episodes/next?key=7c2f686dfaad&v=3.0&id={}".format(serie) for serie in
                series]
        requetes_series = Requete(series, ["episode" for i in range(len(series))], urls, series)
        requetes = requetes_series.run()
        # Nettoyage de la réponse : passage en datetime et ecriture dans la base notification
        s = [i[0] for i in
             self.querydb('select episode_id from notification where user_id=?', args=(current_user.get_id(),))]
        for i in requetes:
            try:
                if requetes[i]['id'] not in s:
                    h, m, s = map(int, requetes[i]['date'].split('-'))
                    notifications = Notification(user_id=current_user.get_id(), serie_id=requetes[i]['show']['id'],
                                                 date_diffusion=datetime(h, m, s),
                                                 serie_name=requetes[i]['show']['title'],
                                                 description=requetes[i]['description'], episode_id=requetes[i]['id'],
                                                 code=requetes[i]['code'], title=requetes[i]['title'])
                    db.session.add(notifications)
            except:
                pass
        db.session.commit()

        return (""), 204

    @route('/notifications', endpoint='messages')
    def index(self):
        """
        Route menant à la page de notifications
        """

        notifications = self.querydb('select * from notification where date_diffusion > ? order by date_diffusion asc',
                                 args=(datetime(2012, 10, 10, 10, 10, 10),))
        current_user.last_message_read_time = datetime.utcnow()
        db.session.commit()
        colonnes = ['id', 'serie_name', 'series_id', 'user_id', 'date_diffusion', 'description', 'episode_id', 'code',
                    'title']
        result = [{colonne: i for colonne, i in zip(colonnes, notification)} for notification in notifications]
        return render_template('messages.html', messages=result)


class MyListView(BaseView):

    @route('/', methods=['GET', 'POST'], endpoint='my_list')
    @login_required
    def index(self):
        """
        Route menant à la page de la liste des séries préférées
        """
        if request.method == 'POST':
            l = literal_eval(request.form.get('button'))
            self.ajout(l)
            return (""), 204
        liste = self.querydb('select * from liste_series where person_id = ? order by serie_name asc',
                         args=(current_user.get_id(),))
        starting = request.args.get('starting', default=' ', type=str)
        page = request.args.get('page', default=1, type=int)
        return render_template('my_list.html', posts=liste, starting=starting, page=page)


class HomeView(BaseView):
    route_base = '/'
    @route('/', methods=['GET', 'POST'], endpoint='index')
    def index(self):
        """
        Route menant au menu d'accueil
        """
        # L'utilisateur identifié peut ajouter une nouvelle série à sa liste
        if request.method == 'POST':
            l = literal_eval(request.form.get('button'))
            self.ajout(l)
            return (""), 204
        # Page d'accueil, affiche 3 séries au hasard
        url = "https://api.betaseries.com/shows/random"
        querystring = {"key": "7c2f686dfaad", "v": "3.0", "nb": "3"}
        posts = requests.request("GET", url, params=querystring).json()["shows"]
        for post in posts:
            if len(post.keys()) == 2:
                post['images'] = {'show': url_for('static', filename='img/logo.png')}
            if len(post["description"]) > 500:
                post["description"] = post["description"][:500] + "..."
            post['ajout'] = self.dans_maliste(post)
        bonjour = ""

        # Si l'utilisateur est authentifié, affiche son nom dans le message de bienvenue
        if current_user.is_authenticated:
            bonjour = current_user.username
        return render_template('home.html', posts=posts, bonjour=bonjour)


class LoggerView(BaseView):
    @route('/login', methods=['GET', 'POST'])
    def login(self):
        """
        Route menant à la page d'identification
        """
        # Si l'utilisateur est déjà identifié, renvoie à la page d'accueil
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        # Sinon, récupère les données envoyées, les compare à la base de donnée
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            # Si les identifiants ne sont pas bons on redirige vers la page de connexion
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('LoggerView:login'))
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            # On redirige vers la page appropriée une fois connecté : l'accueil si arrivé en tapant directement l'url, la page d'origine sinon
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return render_template('login.html', title='Sign In', form=form)


    @route('/logout')
    def logout(self):
        """
        Route activant la déconnexion
        """
        logout_user()
        return redirect(url_for('index'))

    @route('/register', methods=['GET', 'POST'])
    def registering(self):
        """
        Route menant à la page d'inscription
        """
        # Si l'utilisateur est déjà authentifié on retourne la page d'accueil
        if current_user.is_authenticated:
           return redirect(url_for('index'))
        form = RegistrationForm()
        # Si le formulaire est correct on enregistre le nouvel utilisateur dans la base
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('LoggerView:login'))
        return render_template('register.html', title='Register', form=form)


SerieView.register(app, base_class=BaseView)
SeriesView.register(app, base_class=BaseView)
NotificationsView.register(app, base_class=BaseView)
MyListView.register(app, base_class=BaseView)
HomeView.register(app, base_class=BaseView)
LoggerView.register(app, base_class=BaseView)
