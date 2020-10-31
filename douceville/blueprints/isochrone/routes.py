from flask import Blueprint, render_template, jsonify, make_response, request, abort
from jinja2 import TemplateNotFound
from sqlalchemy import not_, distinct
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from douceville.config import Config
from douceville.models import db, Etablissement, Resultat
from douceville.utils import logged, Serializer
from douceville.blueprints.isochrone import isochrone_bp
from douceville.blueprints.isochrone.geographique import (
    calcIsochrone,
    findCoordFromAddress,
)


@isochrone_bp.route("/", methods=["GET"])
def isochrone():
    token = request.args.get("token", "")

    s = Serializer()
    dat = s.deserialize(token)
    dist = dat.pop("dist", 600)
    lat = dat.pop("lat", 1.39396)
    lon = dat.pop("lon", 43.547864)

    center = [lon, lat]
    iso = calcIsochrone(center, dist)

    return jsonify(iso)
