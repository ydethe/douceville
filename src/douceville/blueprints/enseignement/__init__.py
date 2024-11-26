from flask import Blueprint


enseignement_bp = Blueprint("enseignement", __name__, template_folder="templates")

from .routes import *  # noqa: E402, F403
