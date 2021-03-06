FROM python:3.5

MAINTAINER divination-software
# Install uWSGI
RUN pip install uwsgi

# Standard set up Nginx
ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
	&& rm -rf /var/lib/apt/lists/*
# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log
# Finished setting up Nginx

# Make NGINX run on the foreground
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# Copy the modified Nginx conf
COPY ./webServerSettings/nginx.conf /etc/nginx/conf.d/
# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY ./webServerSettings/uwsgi.ini /etc/uwsgi/

# Install Supervisord
RUN apt-get update && apt-get install -y supervisor \
&& rm -rf /var/lib/apt/lists/*
# Custom Supervisord config
COPY ./webServerSettings/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Copy while files to /app dir
COPY . /app

# To enable HTTPS, we need to copy certs and a new nginx.conf
# COPY ./nginx.conf /etc/nginx/conf.d/
COPY ./client-cert.pem /etc/ssl/
COPY ./client-key.pem /etc/ssl/

# Give execution rights to run sim_worker script
RUN chmod +x /app/sim_worker.py

WORKDIR /app
ENV HOME /app

# Install uwsgi Python web server
RUN pip install -r dependencies.txt
RUN python setup_db.py

EXPOSE 8443

# Run the script on container startup
CMD ["sh","./start.sh"]