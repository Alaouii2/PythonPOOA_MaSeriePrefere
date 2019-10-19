"""
    Bonjour vous etes dans __init__, pas mal non ?
    C'est l'endroit d'où le reste de nos paquets peut gérer l'environnement
"""

from flask import Flask
from .views import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session


# Importe les plugins de gestion de la bdd, des logins et des sessions
db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()

# L'initialiseur de module
class Initieur():

    def __init__(self):
        # Charge les options de configuration
        app.config.from_object('config')
        # Connecte sqlalchemy, le login et la session à l'app
        db.init_app(app)
        login_manager.init_app(app)
        sess.init_app(app)

        # Crée une fonction d'initialisation de la base de données en ligne de commande
    @app.cli.command()
    def init_db():
        db.drop_all()
        db.create_all()
        print("initialisation")

initieur = Initieur()
