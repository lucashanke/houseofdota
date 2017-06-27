FROM python:3

WORKDIR /usr/src/houseofdota

COPY .babelrc manage.py package.json requirements.txt webpack.config.js ./

RUN pip install -r requirements.txt

COPY app/ ./app
COPY files/ ./files
COPY houseofdota/ ./houseofdota
COPY infra/ ./infra
COPY public/ ./public

CMD gunicorn houseofdota.wsgi -b 0.0.0.0:80 --log-file -
