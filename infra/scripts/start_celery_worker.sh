#!/bin/bash

source venv/bin/activate
ps -aux | grep 'celery -A houseofdota worker' | awk '{print $2}' | xargs kill -9
celery -A houseofdota worker -l info --autoscale=10,3
