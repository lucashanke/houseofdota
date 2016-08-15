#!/bin/bash

rsync -avR . /opt/houseofdota
cd /opt/houseofdota

source venv/bin/activate
export LC_ALL=C
pip install -r requirements.txt

./manage.py makemigrations app
./manage.py migrate

npm install
npm run build

supervisorctl restart gunicorn
