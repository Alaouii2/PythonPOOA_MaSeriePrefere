"""
    Je suis actuellement le commentaire le plus inutile du monde, quel modele !
"""

from flask_sqlalchemy import SQLAlchemy
from .views import app
import logging as lg


# Create database connection object
db = SQLAlchemy(app)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.Integer(), nullable=False)

    def __init__(self, description, gender):
        self.description = description
        self.gender = gender

def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(Content("This is SPARTAAAAA!!!", 1))
    db.session.add(Content("What's your favorite scary movie ?", 0))
    db.session.commit()
    lg.warning('Database initialized !')
