## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement

### Principes généraux

A chaque évolution de l'une des branches du repository GitHub du projet, un workflow CircleCI
se lance automatiquement. Il comprend plusieurs étapes allant de l'installation des dépendances
du projet et de l'exécution de tests, au déploiement sur Heroku, en passant par la génération 
d'une image Docker et sa publication dans un repository DockerHub.

### Configuration requise

- Un compte Docker avec un repository distant sur DockerHub pour enregistrer l'image publiée. Le
nom du repository doit être identique au nom de l'image, soit username/oc-lettings-tnt78

- Un compte Heroku pour héberger les applications.

- Un compte CircleCI en lien avec le compte GitHub contenant le repository du projet. Trois
variables d'environnement liées au worflow du projet doivent être définies.
```
DOCKER_LOGIN      # Username du compte Docker
DOCKER_PASSWORD   # Mot de passe du compte Docker
HEROKU_API_KEY    # Clé API du compte Heroku
```
- Un fichier config.yml dans le répertoire .circleci à la racine du projet (voir la rubrique
'Etapes du déploiement' pour le détail).

- Un fichier Dockerfile à la racine du projet qui contient les instructions nécessaires à la
création de l'image Docker. En complément un fichier .dockerignore permet de lister les répertoires
ou fichiers à ignorer lors de la copie. Selon que vous souhaitez une image pour une exécution
locale sur votre poste de travail ou pour une application web, utilisez l'une ou l'autre des
instructions CMD.
```
FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
EXPOSE 8000
# Exécution en mode local http://127.0.0.1:8000/
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"] 
# Exécution application web https://nom_app.herokuapp.com/
CMD ["gunicorn", "oc_lettings_site.wsgi"] 
```
- L'exécution de flake8 et pytest nécessitent que les dépendances soient installées au préalable
et figurent dans le fichier requirements.txt à la racine du projet.


### Etapes du déploiement

Extrait du fichier config.yml
```
workflows:
  my-pipeline:
    jobs:
      - install-and-test
      - docker/publish:
          image: $DOCKER_LOGIN/oc-lettings-tnt78
          requires:
            - install-and-test
          filters:
            branches:
              only: master
      - heroku/deploy-via-git:
          app-name: oc-lettings-tnt78
          requires:
            - docker/publish
      - deploy-via-docker:
          requires:
            - install-and-test
          filters:
            branches:
              only: container
```
- La première étape **Install-and-test** installe l'ensemble du projet avec ses dépendances sur
une image Docker Python et exécute flake8 et pytest. En cas d'anomalies identifiées par le linter
ou des tests non concluants, le workflow s'achève en mode 'Failed'.
- La seconde étape **docker/publish** requiert la bonne exécution de l'étape 'Install-and-test',
construit une image Docker du projet sur la base des instructions du fichier Dockerfile et la
publie sur le repository DockerHub.
- La troisième étape **heroku/deploy-via-git** requiert la bonne exécution de l'étape
'docker/publish' et déploie l'application sur Heroku via une copie du repository GitHub du projet,
l'installation des dépendances et la génération des fichiers statiques dans le répertoire défini
dans le fichier settings.py

Les étapes 2 et 3 ne s'exécutent que pour la branche master du projet. L'application déployée sur
Heroku est accessible à l'adresse **https://oc-lettings-tnt78.herokuapp.com/**

- Une quatrième étape **deploy-via-docker** est implémentée pour une branche spécifique du projet
nommée container. Elle requiert la bonne exécution de l'étape 'Install-and-test' et déploie
l'application sur Heroku en mode container Docker, via une image Docker construite sur la base des
instructions du fichier Dockerfile. Attention vous devez au préalable générer les fichiers
statiques avec la commande 'python manage.py collectstatic --noinput', modifier le fichier
Dokerfile pour une exécution de l'image en mode application web et mettre à jour la branche via un
git push. L'application est accessible à l'adresse **https://oc-lettings-container.herokuapp.com/**