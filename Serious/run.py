from app import app, db
from app.models import User, Liste_series, Notification


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Liste_series': Liste_series, 'Notification': Notification}
