"""
Ce script correspond au fichier d'initialisation où notre application est créée
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__) #  Création d' un package appelé app qui hébergera l'application
app.config.from_object(Config)
db = SQLAlchemy(app) # création de la base de données
migrate = Migrate(app, db) # migration de la base de données
login = LoginManager(app) # création et initialisation de Flask login
login.login_view = 'login' # instanciation de la fonction de visualisation

from app import routes, models  # importation des modules qui définiront la structure de la base de données
