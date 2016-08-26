#!/bin/bash

source venv/bin/activate
ps -aux | grep 'celery -A houseofdota beat' | awk '{print $2}' | xargs kill -9
celery -A houseofdota beat -l info
