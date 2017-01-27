[![Stories in Ready](https://badge.waffle.io/DomDomPow/snapventure.png?label=ready&title=Ready)](https://waffle.io/DomDomPow/snapventure)

![](https://infinit8.io/illustrations/snapventure/mapjourneybanneer.jpg)

Il est toujours intéressant pour les curieux d’obtenir des informations additionnelles lorsqu’ils visitent un musée ou qu’ils effectuent une excursion à but éducatif. Nous avons tous ressenti un jour l’excitation d’une chasse au trésor. Et nous nous sommes tous déjà demandé ce que représentent certains monuments et autres œuvres d’art conceptuelles. 

L’interface d’administration mise en place dans le cadre de ce projet permet de proposer une solution : développée avec django et permettant d’accéder aux données au travers d’une API, elle permet la création de parcours dont les étapes sont représentées par des QR codes qui affichent un contenu spécifique lorsqu’ils sont scannés. Il reste de nombreuses améliorations potentielles à apporter mais l’interface d’administration est totalement utilisable et permettra, peut-être, d’offrir des expériences ludiques, intéressantes et éducatives à l’avenir. 


## Arborescence

Le projet contient deux parties distinctes qui sont les suivantes :

 * **snapventure_backend** - L'application django qui permet de créer les parcours et qui fournit l'API
 * **snapventure_frontend** - La petite application mobile Android de test

## Mise en place

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

## Description de l'API

Les ressources de l'API sont les suivantes :

* Journey : Le parcours qui contient les étapes
* Step : Les étapes qui constituent un parcours
* Profile : Les profils utilisateurs
* Inscription : Les inscriptions des utilisateurs à des parcours
python manage.py runserver
