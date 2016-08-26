#!/bin/bash

source venv/bin/activate
ps -aux | grep 'gunicorn houseofdota.wsgi -b 0.0.0.0:80 --log-file -' | awk '{print $2}' | xargs kill -9
gunicorn houseofdota.wsgi -b 0.0.0.0:80 --log-file -
