# Comment faire marcher le code

## Installation des packages requises pour le code
 * Lancer un terminal
 * Créer un environement virtuel python
 * Activer l'environement virtuel sur le terminal
 * Se placer dans le dossier PythonPOOA_MaSeriePrefere
 * Tapper "pip install -r requirements.txt"

## Créer la base de donnée

 * Se placer dans le dossier Serious
 * tapper respectivement "flask db init", "flask db migrate", "flask db upgrade" (vous remarquerez un dossier migrations et un fichier app.db qui se créent)

## Lancer l'application

 * Se placer dans le dossier Serious
 * Si vous êtes sur Windows tapper directement "flask run" dans le terminal, sinon il faut tapper avant "FLASK_APP=run.py flask run"
