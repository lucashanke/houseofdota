# House o' Dota

![alt text](https://houseofdota.herokuapp.com/static/images/slide2-min.png)

House of Dota is a application where you can get several kinds of insights regarding the game current meta. What are the heroes most picked? What are the most powerful hero combos? Besides, we have a recommendation system in order to help you choosing the best hero for your line-up.

## Running with Docker

To build:
```
docker-compose build
```
### App

To run the wep app:
```
docker-compose up app
```
### Beat/Worker for background jobs

To run the beat and worker for the background jobs described in app/tasks.py:
```
docker-compose up beat
```
File with environment variables should be in /opt/houseofdota/.env containing the following variables:

```
DJANGO_SETTINGS_MODULE=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
```

## Running locally

### System requirements:

* Python3
* Node.js
* PostgreSQL - sudo apt install postgresql postgresql-contrib

If you using Ubuntu you need to install the postgres-dev package:

```
sudo apt install postgresql-server-dev-all
```

### Python VirtualEnv

Set the env in the project:

```
sudo pip install virtualenv
virtualenv -p python3 env
```

### Install dependencies:

```
npm install
pip install -r requirements.txt
```

### DB Configuration

The database configuration is informed by the environment variables listed above.

### Run:
	npm run dev
	python manage.py runserver
