FROM ubuntu:14.04

MAINTAINER Le Huu Hoang Gia <hoanggia.lh@gmail.com>

RUN apt-get update
RUN apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python python-mysqldb supervisor

RUN mkdir -p /var/log/nginx/app
RUN mkdir -p /var/log/uwsgi/app/


RUN rm /etc/nginx/sites-enabled/default
COPY flask.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/flask.conf /etc/nginx/sites-enabled/flask.conf
COPY uwsgi.ini /var/www/app/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

copy app /var/www/app
RUN pip install -r /var/www/app/requirements.txt


WORKDIR /var/www/app/config/

RUN rm -rf local.*

WORKDIR /var/www/app

#RUN python migrations.py db upgrade

CMD ["/usr/bin/supervisord"]