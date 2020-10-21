import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # ...
    # SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://cl_user@localhost/maillage"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "etablissements.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "localhost"
    PORT = 8080
    