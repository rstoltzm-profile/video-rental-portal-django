# docs

## env
```bash
source venv/bin/activate
```

## freeze
```bash
pip freeze > requirements.txt
```

## django
```bash
source venv/bin/activate
cd source
python manage.py runserver
```

## django commands using manage.py
```bash
## create app
python manage.py startapp films

## migrate
python manage.py runserver
python manage.py migrate
```

## project setup notes
```bash
python3 -m venv venv
pip install django
django-admin check

## create src and config for webapp
mkdir src
cd src
django-admin startproject config .

## create pages directory
python manage.py startapp pages

## migrate and runserver
python manage.py migrate
python manage.py runserver
```