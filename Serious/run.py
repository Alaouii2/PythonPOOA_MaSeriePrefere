from app import app, db
from app.models import User, Post, Liste_series, Notification


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Liste_series': Liste_series, 'Notification': Notification}
