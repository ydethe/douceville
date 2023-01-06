# docker build -t douceville .
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
RUN apt-get update --allow-releaseinfo-change && apt-get install -yqq --no-install-recommends python3-dev python3-pip gcc g++ libssl-dev libpq-dev vim nano
RUN python3 -m pip install --upgrade pip && pip3 install flask && python3 setup.py develop
# RUN flask db init && flask db migrate -m "Initial migration." && flask db upgrade
CMD /usr/bin/uwsgi /app/etc/uwsgi.ini
