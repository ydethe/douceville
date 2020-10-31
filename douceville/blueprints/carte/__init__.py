from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


carte_bp = Blueprint("carte", __name__, template_folder="templates")

from .routes import *
