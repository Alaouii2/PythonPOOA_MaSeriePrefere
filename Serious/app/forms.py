"""
Ce script contient les zones de formulaires définies comme classe
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """
     Classe utilisée par Flask-WTF pour représenter le formulaire de connexion
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me') # Permettre à l'utilisateur de rester connecté s'il le souhaite
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """"
         Classe utilisée par Flask-WTF pour représenter le formulaire d'inscription
        """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]) # S'assurer que le mot de passe et sa confirmation sont égaux
    submit = SubmitField('Register')

    def validate_username(self, username): #fonction pour valider le nom d'utilisateur
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.') # Erreur levée pour s'assurer que le nom d'utilisateur n'est pas utilisé

    def validate_email(self, email): #fonction pour valider l'adresse mail
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')  # Erreur levée pour s'assurer que l'adresse mail n'est pas utilisé