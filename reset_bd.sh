#! /bin/sh

# sudo -H -u postgres psql -d douceville -c "drop table nature;"
# sudo -H -u postgres psql -d douceville -c "drop table nature,resultat,public.'user',etablissement,alembic_version;"
sudo -H -u postgres psql -c "drop database douceville;"
sudo -H -u postgres createdb douceville
rm -rf migrations/versions/*
# FLASK_INIT_DB=1 flask db init
FLASK_INIT_DB=1 flask db migrate
sudo -H -u postgres psql -d douceville -f /usr/share/postgresql/11/contrib/postgis-2.5/postgis.sql
sudo -H -u postgres psql -d douceville -f /usr/share/postgresql/11/contrib/postgis-2.5/spatial_ref_sys.sql
FLASK_INIT_DB=1 flask db upgrade

python3 setup.py develop --user
python douceville/blueprints/users/manage_users.py add ydethe@gmail.com Te1gpqS --admin
