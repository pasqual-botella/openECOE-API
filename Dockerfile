FROM nginx
RUN apt-get update \
  && apt-get install -y python3-virtualenv python3-pip \
  && rm -rf /var/lib/apt/lists/*
COPY . /app/api
WORKDIR /app/api
RUN virtualenv env
RUN env/bin/pip install -r requirements.txt
RUN env/bin/pip install gunicorn
RUN env/bin/pip install requests
EXPOSE 1081
COPY deploy/api.conf /etc/nginx/conf.d/ecoe-api.conf
COPY deploy/gunicorn.sh /docker-entrypoint.d/99-gunicorn.sh