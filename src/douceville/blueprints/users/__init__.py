from flask import Blueprint


users_bp = Blueprint("users", __name__, template_folder="templates")

from .routes import profile, login, signup, confirm, logout  # noqa: E402, F401
