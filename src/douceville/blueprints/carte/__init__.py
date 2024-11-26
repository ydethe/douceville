from flask import Blueprint


carte_bp = Blueprint("carte", __name__, template_folder="templates")

from .routes import carte, recherche  # noqa: E402, F401
