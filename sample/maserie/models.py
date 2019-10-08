"""
    Je suis actuellement le commentaire le plus inutile du monde, quel modele !
    C'est le module gérant la base de donnée de notre application
"""

from flask_sqlalchemy import SQLAlchemy
from .views import app

# Crée l'objet de connection à la base de donnée
db = SQLAlchemy(app)

# Objet Client
class Client(db.Model):

    id_client = db.Column(db.Integer, primary_key=True)
    adresse_mail = db.Column(db.String(100), nullable=False)
    mdp = db.Column(db.String(20), nullable=False)
    nom_utilisateur = db.Column(db.String(20), nullable=False)

    def __init__(self, adresse_mail, mdp, nom_utilisateur):
        self.adresse_mail = adresse_mail
        self.mdp = mdp
        self.nom_utilisateur = nom_utilisateur


# Objet liste de séries préférées, par utilisateur
class Liste_serie_preferee(db.Model):

    id_liste = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer, db.ForeignKey(Client.id_client))
#    ids_serie = db.Column(db.ARRAY(db.Integer), nullable=True)

    def __init__(self, id_client):
        self.id_client = id_client
#        self.ids_serie = ids_serie

