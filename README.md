![](https://infinit8.io/illustrations/snapventure/mapjourneybanneer.jpg)

Il est toujours intéressant pour les curieux d’obtenir des informations additionnelles lorsqu’ils visitent un musée ou qu’ils effectuent une excursion à but éducatif. Nous avons tous ressenti un jour l’excitation d’une chasse au trésor. Et nous nous sommes tous déjà demandé ce que représentent certains monuments et autres œuvres d’art conceptuelles. 

L’interface d’administration mise en place dans le cadre de ce projet permet de proposer une solution : développée avec django et permettant d’accéder aux données au travers d’une API, elle permet la création de parcours dont les étapes sont représentées par des QR codes qui affichent un contenu spécifique lorsqu’ils sont scannés. Il reste de nombreuses améliorations potentielles à apporter mais l’interface d’administration est totalement utilisable et permettra, peut-être, d’offrir des expériences ludiques, intéressantes et éducatives à l’avenir. 


## Arborescence

Le projet contient deux parties distinctes qui sont les suivantes :

 * **snapventure_backend** - L'application django qui permet de créer les parcours et qui fournit l'API
 * **snapventure_frontend** - La petite application mobile Android de test

## Mise en place

Pour tester l'application en local avec deux utilisateurs et trois simples parcours d'exemples. Chacune de ces étapes est très importante pour que le tout fonctionne correctement.

Clôner le git et se rendre dans le dossier de la partie backend

```
git clone https://github.com/DomDomPow/snapventure.git
cd snapventure/snapventure-backend
```

Créer un environnement virtuel et l'activer

```
virtualenv snapenv
source snapenv/bin/activate
```

Installer les dépendances

```
pip install -r requirements.txt
```

Créer la base de données mysql

```
mysql
>> create database snapventure;
```

Configurer les variables d'environnement

```
# ~/.bashrc

export DJANGO_SECRET_KEY="YOUR_KEY"
export DJANGO_DEBUG=True
export DJANGO_DB_NAME="snapventure"
export DJANGO_DB_USER="root"
export DJANGO_DB_PWD="1234"
export DJANGO_DB_HOST="localhost"

```

Effectuer les migrations et loader les données initiales
```
python manage.py migrate
python manage.py loaddata initial_data.json
```

Lancer le server django

```
python manage.py runserver
```

## Description de l'API

Les ressources de l'API sont les suivantes :
```
http://localhost:8000/api/v1/journey
http://localhost:8000/api/v1/step
http://localhost:8000/api/v1/type
http://localhost:8000/api/v1/scan
http://localhost:8000/api/v1/profile
```
