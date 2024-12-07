# LITRevu

Un gestionnaire de critiques et de tickets interactifs développé avec Django.

---


**LITRevu** est une application web permettant aux utilisateurs de :
- Créer et gérer des tickets.
- Publier des critiques sur des tickets.
- Suivre d'autres utilisateurs et leurs activités.

**LITRevu** is a web application allowing users to:
- Create and manage tickets.
- Post reviews on tickets.
- Follow other users and their activities.

---


- **Python** : version 3.8 ou supérieure / Python 3.8 or higher
- **Git** : pour cloner le projet / to clone the project
- **Pip** : pour installer les dépendances / to install dependencies
- **Virtualenv** : recommandé pour isoler l'environnement / recommended for environment isolation

---

# Installation

#### **1. Clonez le dépôt / Clone the repository**

```
git clone https://github.com/votre-utilisateur/LITRevu.git
cd LITRevu
```

#### **2. Créez et activez un environnement virtuel / Create and activate a virtual environment**

1. Lancer l'environnement / create a virtual environment
Sous Windows / On Windows :

```
python -m venv env
env\Scripts\activate
```

Sous Linux / On Linux :

```
python3 -m venv env
source env/bin/activate
```

2. Installez les dépendances / Install dependencies

```
pip install -r requirements.txt
```

Configurez la base de données / Configure the database


```
python manage.py migrate
```

1. Lancez le serveur de développement / Run the development server
```
python manage.py runserver
```

Accédez à l'application sur http://127.0.0.1:8000.