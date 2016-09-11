#!/bin/bash

deactivate
source /opt/houseofdota/venv/bin/activate
ps -aux | grep 'celery -A houseofdota worker' | awk '{print $2}' | xargs kill -9
exec /opt/houseofdota/venv/bin/celery -A houseofdota worker -l debug --autoscale=5,3 --logfile /var/log/celery/worker.log
