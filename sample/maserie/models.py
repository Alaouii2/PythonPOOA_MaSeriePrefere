"""
    Je suis actuellement le commentaire le plus inutile du monde, quel modele !
    Mais en vrai vous allez voir ca va etre open fun ce module, j'espère que vous allez apprécier !
"""

from flask_sqlalchemy import SQLAlchemy
from .views import app
import datetime

# Create database connection object
db = SQLAlchemy(app)


# class Content(db.Model):
#
#     id = db.Column(db.Integer, primary_key=True)
#     description = db.Column(db.String(200), nullable=False)
#     gender = db.Column(db.Integer(), nullable=False)
#
#     def __init__(self, description, gender):
#         self.description = description
#         self.gender = gender


class Client(db.Model):

    id_client = db.Column(db.Integer, primary_key=True)
    adresse_mail = db.Column(db.String(100), nullable=False)
    mdp = db.Column(db.String(20), nullable=False)
    nom_utilisateur = db.Column(db.String(20), nullable=False)

    def __init__(self, adresse_mail, mdp, nom_utilisateur):
        self.adresse_mail = adresse_mail
        self.mdp = mdp
        self.nom_utilisateur = nom_utilisateur


class Serie_disponible(db.Model):

    id_serie = db.Column(db.Integer, primary_key=True)
    titre_serie = db.Column(db.String(100), nullable=False)
    descriptif_serie = db.Column(db.String(1000), nullable=True)
    nb_saison = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    annee_production = db.Column(db.DateTime, nullable=False)
    realisateur = db.Column(db.String(100), nullable=False)

    def __init__(self, titre_serie, descriptif_serie, nb_saison, genre, annee_production, realisateur):
        self.titre_serie = titre_serie
        self.descriptif_serie = descriptif_serie
        self.nb_saison = nb_saison
        self.genre = genre
        self.annee_production = annee_production
        self.realisateur = realisateur


class Saison(db.Model):

    id_saison = db.Column(db.Integer, primary_key=True)
    id_serie = db.Column(db.Integer, db.ForeignKey(Serie_disponible.id_serie))
    n_saison = db.Column(db.Integer, nullable=False)
    n_episode = db.Column(db.Integer, nullable=False)

    def __init__(self, id_serie, n_saison, n_episode):
        self.id_serie = id_serie
        self.n_saison = n_saison
        self.n_episode = n_episode


class Episode(db.Model):

    id_episode = db.Column(db.Integer, primary_key=True)
    id_saison = db.Column(db.Integer, db.ForeignKey(Saison.id_saison))
    descriptif_episode = db.Column(db.String(1000), nullable=True)
    duree_episode = db.Column(db.DateTime, nullable=False)
    numero_episode = db.Column(db.Integer, nullable=False)

    def __init__(self, id_saison, descriptif_episode, duree_episode, numero_episode):
        self.id_saison = id_saison
        self.descriptif_episode = descriptif_episode
        self.duree_episode = duree_episode
        self.numero_episode = numero_episode


class Liste_serie_preferee(db.Model):

    id_liste = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey(Client.id_client))
#    ids_serie = db.Column(db.ARRAY(db.Integer), nullable=True)

    def __init__(self, id_client, ids_serie):
        self.id_client = id_client
#        self.ids_serie = ids_serie


def init_db():
    db.drop_all()
    db.create_all()
#    db.session.add(Content("This is iughukygv!!!", 1))
#    db.session.add(Content("What's your favorite scary movie ?", 0))

    db.session.add(Client("bonjour@salut.com", "mdp", "username"))
    db.session.add(Serie_disponible("Naruto", "Un ninja pas comme les autres", 10, "ninja", datetime.date(1995, 1, 1), "masashi kishimoto"))
    db.session.add(Serie_disponible("Bleach", "Des hollows à en pleuvoir", 20, "samourai", datetime.date(1997, 3, 5), "shigeru myamoto"))
    db.session.add(Saison(1, 3, 20))
    db.session.add(Episode(1, "Bonjour je suis l'episode 3", datetime.datetime(year=1995, month=12, day=4, hour=22, minute=20), 3))

    db.session.add(Liste_serie_preferee(1))
    db.session.commit()
    client = Client.query.get(1)
    serie = Serie_disponible.query.get(1)
    saison = Saison.query.get(1)
    episode = Episode.query.get(1)
    liste = Liste_serie_preferee.query.get(1)
    print(client.adresse_mail)
    print(serie.titre_serie)
    print(saison.n_episode)
    print(episode.duree_episode)
    print(liste.id_client)



