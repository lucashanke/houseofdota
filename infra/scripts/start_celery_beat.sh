#!/bin/bash

deactivate
source /opt/houseofdota/venv/bin/activate
ps -aux | grep 'celery -A houseofdota beat' | awk '{print $2}' | xargs kill -9
exec /opt/houseofdota/venv/bin/celery -A houseofdota beat -l info --logfile /var/log/celery/beat.log
