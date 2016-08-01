#!/bin/bash

source venv/bin/activate
celery -A houseofdota beat -l info
