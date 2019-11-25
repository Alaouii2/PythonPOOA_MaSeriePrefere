"""
Script pour lancer l'application flask sur terminal (en tappant "flask run")
.flaskenv permet de lancer directement l'application sur le terminal sans faire un FLASK_APP = run.py à chaque
fois.
"""

from app import app, db
from app.models import User, Liste_series, Notification


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Liste_series': Liste_series, 'Notification': Notification}
