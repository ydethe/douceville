from flask_sqlalchemy import SQLAlchemy

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        current_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://cl_user@localhost/etablissements"

        g.db = SQLAlchemy(app)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


