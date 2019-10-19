"""
    C'est le fichier de configuration.
    Pour faire fonctionner Flask, notamment au niveau des chemins relatifs
"""

import os

# Configure le chemin de la base de donnée
SECRET_KEY = "Top secret, mais pour la simplicité de ce tp on va faire simple, surtout qu'en sécurité des systèmes " \
             "d'information on a vu que la sécurité ca signifiait pas grand chose, surtout que pour une appli aussi " \
             "simpliste ce serait un peu overkill"
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
