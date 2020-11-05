from flask import Blueprint


isochrone_bp = Blueprint("isochrone", __name__, template_folder="templates")

from .routes import *
