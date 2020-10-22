import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://ydethe:m41ll4g3@ydethe.mysql.pythonanywhere-services.com/ydethe$maillage"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://cl_user@localhost/maillage"
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "etablissements.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # HOST = "http://ydethe.pythonanywhere.com"
    # PORT = 80
    HOST = "localhost"
    PORT = 5000
    SECRET_KEY = "ITSASECRET"
