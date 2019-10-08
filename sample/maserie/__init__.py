"""
    Bonjour vous etes dans __init__, pas mal non ?
    C'est l'endroit d'où le reste de nos paquets peut gérer l'environnement
"""

from .views import app
from . import models

# Connecte sqlalchemy à l'app
models.db.init_app(app)

# Crée une fonction d'initialisation de la base de données en ligne de commande
@app.cli.command()
def init_db():
    models.init_db()
