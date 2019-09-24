# PythonPOOA_MaSeriePrefere
Le repo pour le projet python Ma série préférée

## Énoncé
Plusieurs API proposent gratuitement une base de données sur les séries TV (vous trouverez plus facilement une version anglophone).
Le projet consiste à créer un site web ou une application qui permet à un utilisateur d’ajouter une série TV à sa liste de séries TV préférées. Une fois dans sa liste, il peut consulter le résumé des épisodes, avoir une alerte lorsque la prochaine diffusion approche.
L’application devra forcément avoir une interface graphique.

## Cahier des charges
Interface graphique. Soit : 
* Interface web
  * Django
  * Flask

* Client lourd
  * PyQT
  * Tkinter

Compte client avec :
* Liste de série préférée
* Résumés des épisodes
* Alerte de la prochaine diffusion d'un épisode d'une série dans la liste

Utilitaires :
* Liste de série via des api des bases de données de séries
* Possibilité d'ajout à sa liste

## Détails fonctionels
Tri des séries : en fonction du contenu des API
* Alphabétique
* Catégories
* Plateforme
* etc...

Liste des API :
* https://api.thetvdb.com/swagger
* https://api.betaseries.com