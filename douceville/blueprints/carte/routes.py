from flask import Blueprint, render_template, jsonify, make_response, request, abort
from jinja2 import TemplateNotFound
from sqlalchemy import not_, distinct
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from douceville.config import Config
from douceville.models import db, Etablissement, Resultat
from douceville.geographique import calcIsochrone, findCoordFromAddress
from douceville.utils import logged, Serializer
from douceville.blueprints.carte import carte_bp


@carte_bp.route("/", methods=["GET"])
def carte():
    year = int(request.args.get("year", "2018"))
    nature = request.args.get("nature", "0")
    departement = int(request.args.get("departement", "0"))
    stat_min = int(request.args.get("stat_min", "0"))
    dist = float(request.args.get("dist", "300"))
    lon = float(request.args.get("lon", "1.39396"))
    lat = float(request.args.get("lat", "43.547864"))
    address = request.args.get("address", "")

    if address != "":
        lon, lat = findCoordFromAddress(address)

    s = Serializer()
    dat = {
        "year": year,
        "nature": nature,
        "departement": departement,
        "dist": dist,
        "lon": lon,
        "lat": lat,
        "stat_min": stat_min,
    }
    token = s.serialize(dat)

    return render_template(
        "carte/carte.html",
        points_request="%s:%i/enseignement?token=%s" % (Config.HOST, Config.PORT, token),
        isochrone_request="%s:%i/isochrone?token=%s"
        % (Config.HOST, Config.PORT, token),
    )
