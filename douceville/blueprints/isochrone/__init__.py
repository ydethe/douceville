from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


isochrone_bp = Blueprint("isochrone", __name__, template_folder="templates")

from .routes import *
