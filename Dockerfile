# Stage 1: Build
FROM python:3.11-alpine

ARG LOGIN_DISABLED
ARG LOGFIRE_TOKEN
ARG LOGLEVEL
ARG FLASK_ADMIN_SWATCH
ARG BCRYPT_ROUNDS
ARG SECRET_KEY
ARG OPENROUTESERVICE_KEY
ARG STRIPE_SECRET_KEY
ARG STRIPE_PUBLISHABLE_KEY
ARG ADMIN_EMAIL
ARG ADMIN_PASSWORD
ARG MAIL_SERVER
ARG MAIL_PORT
ARG MAIL_USE_TLS
ARG MAIL_USE_SSL
ARG MAIL_USERNAME
ARG MAIL_PASSWORD
ARG MAIL_DEFAULT_SENDER
ARG ADDOK_HOST
ARG POSTGRES_HOST
ARG POSTGRES_DB
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG HOST
ARG API_PATH
ARG PRICE_ID
ARG GITHUB_CLIENT_ID
ARG GITHUB_CLIENT_SECRET

ENV LOGIN_DISABLED=$LOGIN_DISABLED
ENV LOGFIRE_TOKEN=$LOGFIRE_TOKEN
ENV LOGLEVEL=$LOGLEVEL
ENV FLASK_ADMIN_SWATCH=$FLASK_ADMIN_SWATCH
ENV BCRYPT_ROUNDS=$BCRYPT_ROUNDS
ENV SECRET_KEY=$SECRET_KEY
ENV OPENROUTESERVICE_KEY=$OPENROUTESERVICE_KEY
ENV STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
ENV STRIPE_PUBLISHABLE_KEY=$STRIPE_PUBLISHABLE_KEY
ENV ADMIN_EMAIL=$ADMIN_EMAIL
ENV ADMIN_PASSWORD=$ADMIN_PASSWORD
ENV MAIL_SERVER=$MAIL_SERVER
ENV MAIL_PORT=$MAIL_PORT
ENV MAIL_USE_TLS=$MAIL_USE_TLS
ENV MAIL_USE_SSL=$MAIL_USE_SSL
ENV MAIL_USERNAME=$MAIL_USERNAME
ENV MAIL_PASSWORD=$MAIL_PASSWORD
ENV MAIL_DEFAULT_SENDER=$MAIL_DEFAULT_SENDER
ENV ADDOK_HOST=$ADDOK_HOST
ENV POSTGRES_HOST=$POSTGRES_HOST
ENV POSTGRES_DB=$POSTGRES_DB
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV HOST=$HOST
ENV API_PATH=$API_PATH
ENV PRICE_ID=$PRICE_ID
ENV GITHUB_CLIENT_ID=$GITHUB_CLIENT_ID
ENV GITHUB_CLIENT_SECRET=$GITHUB_CLIENT_SECRET

ENV SQLALCHEMY_TRACK_MODIFICATIONS=False

RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev geos-dev

WORKDIR /code

COPY dist/*.whl /code
RUN pip install -U /code/*.whl && rm -f /code/*.whl
EXPOSE 3566
CMD ["hypercorn", "douceville.rest_api_entreypoint:app", "--bind", "0.0.0.0:3566"]
