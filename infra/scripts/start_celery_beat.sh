#!/bin/bash

source venv/bin/activate
celery -A houseofdota worker -l info
