web: gunicorn houseofdota.wsgi --log-file -
worker: celery -A houseofdota worker -l info
worker: celery -A houseofdota beat -l info
