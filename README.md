# {{ project_name }}

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites groups
./manage.py runserver
```

celery -A ET worker -l info
