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
cd videoportal
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