from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from time import time
import json


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    series = db.relationship('Liste_series', backref='user', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def new_messages(self):
        self.last_message_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Notification.query.filter(Notification.date_diffusion > self.last_message_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(serie_name=name, description=json.dumps(data), user=self)
        db.session.add(n)
        return n

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Liste_series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    serie_id = db.Column(db.Integer)
    serie_name = db.Column(db.String(100))
    serie_pictureurl = db.Column(db.String(100))

# Setup the relationship to the User table
    users = db.relationship(User)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie_name = db.Column(db.String(128))
    serie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_diffusion = db.Column(db.DateTime, default=time)
    description = db.Column(db.Text)
    episode_id = db.Column(db.Integer)
    code = db.Column(db.String(40), index=True)
    title = db.Column(db.Text)

    #def get_data(self):
    #    return json.loads(str(self.payload_json))