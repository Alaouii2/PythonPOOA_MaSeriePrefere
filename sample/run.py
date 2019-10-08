#! /usr/bin/env python

"""
    Ce module est absolument incroyable, c'est run
    C'est le point d'entrée de notre application
"""

from maserie import app

# Lance l'application Flask depuis le fichier views
if __name__ == "__main__":
    app.run(debug=True)
