from flask import Blueprint


payment_bp = Blueprint("payment", __name__, static_folder="js", template_folder="templates")

from .routes import *  # noqa: E402, F403
