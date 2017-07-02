FROM houseofdota:base

COPY ../package.json ./
RUN npm install
RUN npm run build

CMD gunicorn houseofdota.wsgi -b 0.0.0.0:80 --log-file -
