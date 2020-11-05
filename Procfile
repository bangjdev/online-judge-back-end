release: python manage.py migrate --run-syncdb
worker: celery -A online_judger_backend worker -l info
web: gunicorn online_judger_backend.wsgi