#! /usr/bin/env python

"""
    Ce module est absolument incroyable, c'est run
    C'est le point d'entrée de notre application
"""

from maserie import app

# Le runner de notre application
class Runner():

    # Lance l'application Flask depuis le fichier views
    def __init__(self):
        if __name__ == "__main__":
            app.run(debug=True)

runner = Runner()