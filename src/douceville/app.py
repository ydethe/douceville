import logfire
from sqlalchemy import select
import stripe
from sqlalchemy.orm import Session

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_login import current_user
from flask_nav3 import Nav
from flask_nav3.elements import View, Navbar
from flask_admin.contrib.sqla import ModelView

from .blueprints.users import users_bp
from .blueprints.carte import carte_bp
from .blueprints.isochrone import isochrone_bp
from .blueprints.payment import payment_bp
from .blueprints.enseignement import enseignement_bp

from .config import config


class UserModelView(ModelView):
    def is_accessible(self):
        return current_user.active and current_user.is_authenticated and current_user.admin

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for("users.login"))


def test_db_filled() -> bool:
    import sqlalchemy as sa
    from .models import get_engine

    engine = get_engine()
    insp = sa.inspect(engine)
    return insp.has_table("resultat", schema="dbo")


# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)

bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
logfire.instrument_flask(app)


@login_manager.user_loader
def load_user(userid):
    from .models import User, get_engine

    engine = get_engine()
    with Session(engine) as session:
        stmt = select(User).where(User.id == userid)
        user = session.scalars(stmt).first()

    return user


stripe.api_key = config.STRIPE_SECRET_KEY


@app.route("/")
def accueil():
    return redirect(url_for("carte.carte"))


if not test_db_filled():
    from . import logger
    from .models import Base, get_engine
    from .blueprints.users.manage_users import add_user

    logger.info("Initializing database: table creation...")

    engine = get_engine()
    Base.metadata.create_all(engine)

    add_user(
        login="ydethe",
        email=config.ADMIN_EMAIL,
        pwd=config.ADMIN_PASSWORD,
        admin=True,
        active=True,
    )

    logger.info("Database tables created")

app.register_blueprint(carte_bp, url_prefix="/carte")
app.register_blueprint(users_bp, url_prefix="/users/")
app.register_blueprint(isochrone_bp, url_prefix="/isochrone")
app.register_blueprint(payment_bp, url_prefix="/pay")
app.register_blueprint(enseignement_bp, url_prefix="/enseignement")

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
