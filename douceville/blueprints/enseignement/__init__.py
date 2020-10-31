from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


enseignement_bp = Blueprint("enseignement", __name__, template_folder="templates")

from .routes import *
