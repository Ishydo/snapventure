# Snapventure

Une interface web qui permet de créer des parcours dont les étapes sont des représentées par des qrcodes. 

La partie backend django fourni l'API et les pages permettant la création de nouveaux parcours dans lesquels se trouvent les étapes. Un concept adapté aux lieux publics présentant des expositions, pour des événements spéciaux ou tout simplement pour organiser des chasses au trésor à la maison.

## Description de l'API

Les ressources de l'API sont les suivantes :

* Journey : Le parcours qui contient les étapes
* Step : Les étapes qui constituent un parcours
* Profile : Les profils utilisateurs
* Inscription : Les inscriptions des utilisateurs à des parcours


## Utiliser le backend snapventure

Clôner le git

```
git clone https://github.com/DomDomPow/snapventure.git
```


Se rendre dans le dossier de la partie backend


```
cd snapventure/snapventure-backend
```


Créer un environnement virtuel 

```
virtualenv snapenv
```

Activer l'environnement

```
source snapenv/bin/activate
```

Installer les dépendances

```
pip install -r requirements.txt
```


Loader les données de démo (+TODO epliquer db & migrations)

```
python manage.py loaddata testjourney
```

Lancer le server django

```
python manage.py runserver
```
