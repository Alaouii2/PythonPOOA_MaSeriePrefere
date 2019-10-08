"""
    C'est le fichier de configuration.
    Pour faire fonctionner Flask, notamment au niveau des chemins relatifs
"""

import os

# Configure le chemin de la base de donnée
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
