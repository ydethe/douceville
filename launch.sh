#! /bin/sh

gunicorn --certfile /home/user-data/ssl/ssl_certificate.pem --keyfile  /home/user-data/ssl/ssl_private_key.pem -b 0.0.0.0:8123 maillage:app

