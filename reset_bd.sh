#! /bin/sh

POSTGIS_PATH=/Applications/Postgres.app/Contents/Versions/latest/share/postgresql/contrib/postgis-3.1

psql -U postgres -c "drop database douceville;"
createdb douceville
rm -rf migrations/versions/*
FLASK_INIT_DB=1 flask db migrate
psql -U postgres -d douceville -f $POSTGIS_PATH/postgis.sql
psql -U postgres -d douceville -f $POSTGIS_PATH/spatial_ref_sys.sql
FLASK_INIT_DB=1 flask db upgrade

python3 setup.py develop --user
python douceville/blueprints/users/manage_users.py add ydethe@gmail.com Te1gpqS --admin --active


