import requests

url = "https://api.betaseries.com/shows/list"

querystring = {"key":"7c2f686dfaad","v":"3.0","limit":"10"}

response = requests.request("GET", url, params=querystring)

# Liste des series disponibles
print(response.json())

# Fonction d'ajout à sa liste : créer une api interne puis POST


# Liste de série préférée : créer une api interne puis GET


# Résumés des épisodes précédents : GET la série en question et notamment ses épisodes et résumés (pas interne)


# Alerte de la prochaine diffusion : GET les épisodes des séries (interne) et les ranger dans un tableau,
# Quand la date est moins d'une semaine, envoyer un message dans un panneau notif

