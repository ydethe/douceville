# docker build -t douceville . --network=host
# docker tag douceville:latest ydethe/douceville:latest
# docker push ydethe/douceville:latest
FROM ubuntu:jammy
COPY . /app/
WORKDIR /app
SHELL ["/bin/bash", "-c"]
RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true
RUN echo "tzdata tzdata/Areas select Europe" > preseed.txt
RUN echo "tzdata tzdata/Zones/Europe select Berlin" >> preseed.txt
RUN debconf-set-selections preseed.txt
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
RUN apt-get update --allow-releaseinfo-change && apt-get install -yqq --no-install-recommends python3-dev python3-pip gnupg2 gcc g++ libssl-dev libpq-dev vim nano postgis postgresql-13-postgis-3 postgresql-13-postgis-3-scripts
RUN python3 -m pip install --upgrade pip && pip3 install flask && python3 setup.py develop
RUN flask db init && flask db migrate -m "Initial migration." && flask db upgrade
CMD /usr/bin/uwsgi /app/etc/uwsgi.ini
