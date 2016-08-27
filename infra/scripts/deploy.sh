#!/bin/bash

echo 'Copying source files to /opt/houseofdota...'

rsync -avR . /opt/houseofdota
cd /opt/houseofdota

echo 'Activating virtual environment (venv)...'

source venv/bin/activate
export LC_ALL=C

echo 'Installing Python dependencies...'

pip install -r requirements.txt

echo 'Migrating database...'

./manage.py makemigrations app
./manage.py migrate

echo 'Installing JS dependencies...'

npm install

echo 'Building JS/CSS assets...'

npm run build

echo 'Configuring supervisor...'

cp infra/supervisor/houseofdota.conf /etc/supervisor/conf.d/

echo 'Restarting services (gunicorn, beat, workers)...'

supervisorctl restart gunicorn beat worker
