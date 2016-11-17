# Snapventure

Une interface web permettant de créer des parcours dont les étapes sont des **qrcodes**.

Contient la partie backend avec l'api et les pages permettant la création des parcours ainsi qu'un petit client permettant de tester.


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

Installer les dépendances

```
pip install -r requirements.txt
```


Loader les données de démo (+db & migrations)

```
python manage.py loaddata testjourney
```

Lancer le server django

```
python manage.py runserver
```
