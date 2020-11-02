"""
   Manipulation of algebraic numbers
   Y. de The
"""
from pkg_resources import get_distribution
import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from sqlalchemy import event

from douceville.config import Config
from douceville.DVLogFormatter import DVLogFormatter


try:
    __version__ = get_distribution(__name__).version
except Exception as e:
    __version__ = "dev"

__author__ = "Y. de The"
__email__ = "yann@johncloud.fr"


# création de l'objet logger qui va nous servir à écrire dans les logs
logger = logging.getLogger("douceville_logger")
# on met le niveau du logger à DEBUG, comme ça il écrit tout
logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.INFO)

# création d'un formateur qui va ajouter le temps, le niveau
# de chaque message quand on écrira un message dans le log
formatter = DVLogFormatter()
# création d'un handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

file_handler = RotatingFileHandler("douceville.log", maxBytes=10e6, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

if os.environ.get('FLASK_INIT_DB','0') == '0':
    from douceville.blueprints.carte import carte_bp

    app.register_blueprint(carte_bp, url_prefix="/carte")

    from douceville.blueprints.isochrone import isochrone_bp

    app.register_blueprint(isochrone_bp, url_prefix="/isochrone")

    from douceville.blueprints.enseignement import enseignement_bp

    app.register_blueprint(enseignement_bp, url_prefix="/enseignement")

    admin = Admin(app, name="douceville", template_mode="bootstrap3")

    from douceville import routes, models

    admin.add_view(ModelView(models.Etablissement, db.session))
    admin.add_view(ModelView(models.Resultat, db.session))
