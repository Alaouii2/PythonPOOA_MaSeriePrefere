"""
    Je suis actuellement le commentaire le plus inutile du monde, quel modele !
    Mais en vrai vous allez voir ca va etre open fun ce module, j'espère que vous allez apprécier !
"""

from flask_sqlalchemy import SQLAlchemy
from .views import app


# Create database connection object
db = SQLAlchemy(app)

class Content(db.Model):
    """
        Adds two numbers and returns the result.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.Integer(), nullable=False)

    def __init__(self, description, gender):
        """
            Adds two numbers and returns the result.
        """
        self.description = description
        self.gender = gender

    def quelconque(self):
        """
        Test
        :return: rien
        """
        pass

def init_db():
    """
            Adds two numbers and returns the result.

        This add two real numbers and return a real result. You will want to
        use this function in any place you would usually use the ``+`` operator
        but requires a functional equivalent.

        :param a: The first number to add
        :param b: The second number to add
        :type a: int
        :type b: int
        :return: The result of the addition
        :rtype: int

        :Example:

        >>> add(1, 1)
        2
        >>> add(2.1, 3.4)  # all int compatible types work
        5.5

        .. seealso:: sub(), div(), mul()
        .. note:: You may want to use a lambda function instead of this.
    """
    db.drop_all()
    db.create_all()
    db.session.add(Content("This is iughukygv!!!", 1))
    db.session.add(Content("What's your favorite scary movie ?", 0))
    db.session.commit()
    logger.warning('Database initialized !')
