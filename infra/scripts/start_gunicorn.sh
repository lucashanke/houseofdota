#!/bin/bash

source venv/bin/activate
gunicorn houseofdota.wsgi -b 0.0.0.0:80 --log-file -
