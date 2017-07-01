FROM python:3

WORKDIR /usr/src/houseofdota

RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get update & apt-get install -y nodejs

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY app/ ./app
COPY files/ ./files
COPY houseofdota/ ./houseofdota
COPY infra/ ./infra
COPY public/ ./public
COPY .babelrc manage.py webpack.config.js ./

RUN mkdir /var/log/celery
