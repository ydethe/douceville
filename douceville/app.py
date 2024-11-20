import stripe
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_login import current_user
from flask_nav3 import Nav
from flask_nav3.elements import View, Navbar
from flask_alembic import Alembic

# from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .blueprints.users import users_bp
from .blueprints.carte import carte_bp
from .blueprints.isochrone import isochrone_bp
from .blueprints.payment import payment_bp
from .blueprints.enseignement import enseignement_bp

# from . import models
from .config import config
from . import logger


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.active and current_user.is_authenticated and current_user.admin

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for("users.login"))


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

alembic = Alembic()
alembic.init_app(app)  # call in the app factory if you're using that pattern

stripe.api_key = config.STRIPE_SECRET_KEY


@app.route("/")
def accueil():
    return redirect(url_for("carte.carte"))


if config.FLASK_INIT_DB:
    logger.info("Initializing database: table creation...")
    with app.app_context():
        db.create_all()
    logger.info("Done")

app.register_blueprint(carte_bp, url_prefix="/carte")
app.register_blueprint(users_bp, url_prefix="/users/")
app.register_blueprint(isochrone_bp, url_prefix="/isochrone")
app.register_blueprint(payment_bp, url_prefix="/pay")
app.register_blueprint(enseignement_bp, url_prefix="/enseignement")

# admin = Admin(app, name="douceville", template_mode="bootstrap3")

# admin.add_view(UserModelView(models.Etablissement, db.session))
# admin.add_view(UserModelView(models.Nature, db.session))
# admin.add_view(UserModelView(models.Resultat, db.session))
# admin.add_view(UserModelView(models.User, db.session))

topbar = Navbar(
    "douceville.fr",
    View("Carte", "carte.carte"),
    View("Recherche", "carte.recherche"),
    View("Profil", "users.profile"),
)

# registers the "top" menubar
nav = Nav()
nav.register_element("top", topbar)
nav.init_app(app)
