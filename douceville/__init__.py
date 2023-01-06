"""
   Manipulation of algebraic numbers
   Y. de The
"""
from pkg_resources import get_distribution
import logging
from logging.handlers import RotatingFileHandler
import os

import stripe
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_login import current_user
from flask_nav import Nav
from flask_nav.elements import *

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
formatter = DVLogFormatter(notime=True)
# création d'un handler qui va rediriger chaque écriture de log
# sur la console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

formatter = DVLogFormatter(notime=False)
file_handler = RotatingFileHandler("douceville.log", maxBytes=10e6, backupCount=5)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
app.logger.addHandler(file_handler)

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

stripe.api_key = Config.STRIPE_SECRET_KEY

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.active and current_user.is_authenticated and current_user.admin

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for("users.login"))


@app.route("/")
def accueil():
    return redirect(url_for("carte.carte"))


if os.environ.get("FLASK_INIT_DB", "0") != "0":
    db.init_app(app)
    db.create_all()

# from douceville.blueprints.carte import carte_bp

# app.register_blueprint(carte_bp, url_prefix="/carte")

# from douceville.blueprints.users import users_bp

# app.register_blueprint(users_bp, url_prefix="/users/")

# from douceville.blueprints.isochrone import isochrone_bp

# app.register_blueprint(isochrone_bp, url_prefix="/isochrone")

# from douceville.blueprints.payment import payment_bp

# app.register_blueprint(payment_bp, url_prefix="/pay")

# from douceville.blueprints.enseignement import enseignement_bp

# app.register_blueprint(enseignement_bp, url_prefix="/enseignement")

# admin = Admin(app, name="douceville", template_mode="bootstrap3")

# from douceville import models

# admin.add_view(UserModelView(models.Etablissement, db.session))
# admin.add_view(UserModelView(models.Nature, db.session))
# admin.add_view(UserModelView(models.Resultat, db.session))
# admin.add_view(UserModelView(models.User, db.session))

# topbar = Navbar(
#     "douceville.fr",
#     View("Carte", "carte.carte"),
#     View("Recherche", "carte.recherche"),
#     View("Profil", "users.profile"),
# )

# # registers the "top" menubar
# nav = Nav()
# nav.register_element("top", topbar)

# nav.init_app(app)
