# docker build -t douceville . --network=host
# docker tag douceville:latest ydethe/douceville:latest
# docker push ydethe/douceville:latest
FROM python:3.9-bullseye

ARG SECRET_KEY
ARG OPENROUTESERVICE_KEY
ARG STRIPE_SECRET_KEY
ARG STRIPE_PUBLISHABLE_KEY
ARG MAIL_SERVER
ARG MAIL_PORT
ARG MAIL_USE_TLS
ARG MAIL_USE_SSL
ARG MAIL_USERNAME
ARG MAIL_PASSWORD
ARG MAIL_SENDER_NAME
ARG MAIL_SENDER_EMAIL
ARG DATABASE_URI
ARG HOST
ARG PORT
ARG PRICE_ID

ENV SECRET_KEY $SECRET_KEY
ENV OPENROUTESERVICE_KEY $OPENROUTESERVICE_KEY
ENV STRIPE_SECRET_KEY $STRIPE_SECRET_KEY
ENV STRIPE_PUBLISHABLE_KEY $STRIPE_PUBLISHABLE_KEY
ENV MAIL_SERVER $MAIL_SERVER
ENV MAIL_PORT $MAIL_PORT
ENV MAIL_USE_TLS $MAIL_USE_TLS
ENV MAIL_USE_SSL $MAIL_USE_SSL
ENV MAIL_USERNAME $MAIL_USERNAME
ENV MAIL_PASSWORD $MAIL_PASSWORD
ENV MAIL_SENDER_NAME MAIL_SENDER_NAME
ENV MAIL_SENDER_EMAIL MAIL_SENDER_EMAIL
ENV DATABASE_URI $DATABASE_URI
ENV HOST $HOST
ENV PORT $PORT
ENV PRICE_ID $PRICE_ID

SHELL ["/bin/bash", "-c"]
RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
RUN echo "tzdata tzdata/Areas select Europe" > preseed.txt
RUN echo "tzdata tzdata/Zones/Europe select Berlin" >> preseed.txt
RUN debconf-set-selections preseed.txt
RUN apt-get update --allow-releaseinfo-change && apt-get install -yqq --no-install-recommends python3-dev python3-pip python3-venv gcc g++ gnupg2 libssl-dev libpq-dev curl libgeos-dev libpq-dev
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -
COPY . /app/
WORKDIR /app
RUN mkdir -p log
RUN /root/.local/bin/pdm install --prod
EXPOSE 3031
CMD /app/.venv/bin/gunicorn --access-logfile log/douceville-access.log --error-logfile log/douceville-error.log --workers 3 --bind 0.0.0.0:3031 douceville:app
