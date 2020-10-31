import json

from flask import Blueprint, render_template, jsonify, make_response, request, abort
from jinja2 import TemplateNotFound
from sqlalchemy import not_, distinct
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from douceville.config import Config
from douceville.models import db, Etablissement, Resultat
from douceville.utils import logged, Serializer
from douceville.blueprints.enseignement import enseignement_bp
from douceville.blueprints.isochrone.geographique import calcIsochrone


@enseignement_bp.route("/", methods=["GET"])
def enseignement():
    token = request.args.get("token", "")

    s = Serializer()
    dat = s.deserialize(token)
    print(dat)

    year = dat.pop("year", 2018)
    lat = dat.pop("lat", 1.39396)
    lon = dat.pop("lon", 43.547864)
    dist = dat.pop("dist", 600)
    academie = dat.pop("academie", 'all')
    nature = dat.pop("nature", ["all"])
    secteur = dat.pop("secteur", ["all"])
    departement = dat.pop("departement", "all")
    stat_min = dat.pop("stat_min", 0)

    center = [lon, lat]
    iso = calcIsochrone(center, dist)

    pts = iso["features"][0]["geometry"]["coordinates"][0]

    pg = "POLYGON(("
    for lon, lat in pts:
        pg += "%f %f," % (lon, lat)
    pg = pg[:-1] + "))"

    a = Etablissement.query.filter(not_(Etablissement.position.is_(None))).filter(
        func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg))
    )

    if departement != "all":
        a = a.filter(Etablissement.departement == int(departement))

    if nature != [] and nature != "all":
        a = a.filter(Etablissement.nature == nature[0])

    if secteur != [] and secteur != "all":
        a = a.filter(Etablissement.secteur == secteur[0])

    features = []
    for e in a.all():
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
