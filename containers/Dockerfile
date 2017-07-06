FROM python:3

WORKDIR /usr/src/houseofdota

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get update & apt-get install -y nodejs

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY package.json ./
RUN npm install

COPY files/ ./files
COPY public/ ./public
COPY houseofdota/ ./houseofdota
COPY app/ ./app
COPY .babelrc manage.py webpack.config.js ./

RUN npm run build

RUN mkdir /var/log/celery

CMD gunicorn houseofdota.wsgi -b 0.0.0.0:80 --log-file -
