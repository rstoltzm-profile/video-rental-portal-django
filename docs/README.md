# docs

## env
```bash
source venv/bin/activate
cd src
make webapp-run
```

## freeze
```bash
pip freeze > requirements.txt
```

## django
```bash
source venv/bin/activate
cd src
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

## Project Overview

The Video Rental Portal is a Django-based web interface that provides a user-friendly frontend for a video rental API. The application allows users to manage films, customers, rentals, stores, and payments through a web interface.

## Project Structure

```
video-rental-portal-django/
├── docs/                          # Documentation
│   ├── api-info.md               # API reference information
│   └── development-guide.md      # This file
├── src/                          # Source code
│   ├── config/                   # Django settings and configuration
│   │   ├── settings.py          # Main Django settings
│   │   ├── urls.py              # Root URL configuration
│   │   ├── wsgi.py              # WSGI configuration
│   │   └── asgi.py              # ASGI configuration
│   ├── pages/                    # Page views and templates
│   │   ├── templates/           # HTML templates
│   │   ├── views.py             # View functions
│   │   ├── urls.py              # Page URL patterns
│   │   └── models.py            # Page-specific models
│   ├── up/                       # Health check and API monitoring
│   │   └── views.py             # Health check endpoints
│   ├── manage.py                # Django management script
│   └── db.sqlite3               # SQLite database
├── requirements.txt              # Python dependencies
└── README.md                    # Project documentation
```
