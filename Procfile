web: gunicorn houseofdota.wsgi --log-file -
worker: celery -A houseofdota worker -l info
beat: celery -A houseofdota beat -l info
