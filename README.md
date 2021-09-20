# Deutsch Worte

## Quick start:

### Create virtual env
 1. `virtualenv -p python3 venv`
 2. `workon venv`

### Install requirements
1. `pip install -r requirements.txt`

### Make migrations
1. `cd src`
2. `py manage.py makemigrations`
3. `py manage.py migrate`

### Create superuser
1. `py manage.py createsuperuser`

### Run server
1. `py manage.py runserver`