# houseofdota

*Install and Configure

System requirements:
*Python3
*Postgresql - sudo apt install postgresql postgresql-contrib

Setting project env:
	sudo pip install virtualenv
	virtualenv -p python3 env

Install front dependencies:
	npm install

Application dependencies:
	pip install -r requirements.txt
	pip install python-celery

If you using Ubuntu you need to install the postgres-dev package:
	sudo apt install postgresql-server-dev-all 

The database configuration can be changed in the follow file:
houseofdota/houseofdota/settings.py

Run:
	npm run-script dev
	python manage.py runserver
	
