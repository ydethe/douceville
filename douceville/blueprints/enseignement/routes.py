import json
import logging

from flask import jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import not_
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from douceville.config import Config
from douceville.models import *
from douceville.utils import logged, Serializer
from douceville.blueprints.enseignement import enseignement_bp
from douceville.blueprints.isochrone.geographique import calcIsochrone


@enseignement_bp.route("/", methods=["GET"])
@login_required
def enseignement():
    logger = logging.getLogger("douceville_logger")
    token = request.args.get("token", "")
    if token == '':
        return jsonify({})

    s = Serializer()
    dat = s.deserialize(token)

    year = dat.get("year", 2018)
    lat = dat.get("lat", 1.39396)
    lon = dat.get("lon", 43.547864)
    dist = dat.get("dist", 600)
    transp = dat.get("transp", "")
    nature = dat.get("nature", [])
    secteur = dat.get("secteur", [])
    stat_min = dat.get("stat_min", 0)

    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    pts = iso["features"][0]["geometry"]["coordinates"][0]

    pg = "POLYGON(("
    for lon, lat in pts:
        pg += "%f %f," % (lon, lat)
    pg = pg[:-1] + "))"

    a = (
        db.session.query(Etablissement, Nature)
        .filter(Etablissement.UAI == Nature.etablissement_id)
        .filter(func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg)))
    )

    if nature != []:
        a = a.filter(Nature.nature.in_(nature))

    if secteur != []:
        a = a.filter(Etablissement.secteur.in_(secteur))

    features = []
    for e, n in a.all():
        info = "<b>[%s]%s</b>" % (e.UAI, e.nom)

        stat = 0
        for res in e.resultats:
            if not res.admis is None and res.annee == int(year):
                stat = int(100 * res.admis / res.presents)
                info += "<br>Réussite %s %i : %i%%" % (res.diplome, res.annee, stat)

        if stat >= float(stat_min):
            p = to_shape(e.position)
            lon, lat = p.coords.xy
            f = {
                "geometry": {"coordinates": [lon[0], lat[0]], "type": "Point"},
                "properties": {"info": info},
                "type": "Feature",
            }
            features.append(f)

    return jsonify(features)
