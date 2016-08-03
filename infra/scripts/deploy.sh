#!/bin/bash

rsync -R . /opt/houseofdota
cd /opt/houseofdota

pip install -r requirements.txt

rm -rf node_modules/
npm install
npm run build

supervisorctl restart gunicorn
