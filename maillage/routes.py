import os

from sqlalchemy import not_, or_

from flask import render_template, jsonify
from geojson import Feature, Point, FeatureCollection
import geojson

from maillage.config import basedir
from maillage import app
from maillage.models import Etablissement, Resultat


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    return render_template("index.html", title="Home", user=user)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/points", methods=["GET"])
def get_all_points():
    a = (
        Etablissement.query
        # .filter(Etablissement.departement == 31)
        .filter(not_(Etablissement.latitude.is_(None))).all()
    )
    print(a)

    features = []
    for e in a:
        info = "<b>%s</b><br>" % e.nom

        stat_brevet = 0
        stat_bac = 0

        results = (
            Resultat.query.filter(Resultat.etablissement_id == e.UAI)
            .filter(Resultat.annee == 2018)
            .all()
        )
        for res in results:
            if not res.admis is None:
                stat = res.admis / res.presents
                info += "Réussite %s : %i%%" % (res.diplome, 100 * stat)

        f = {
            "geometry": {"coordinates": [e.longitude, e.latitude], "type": "Point"},
            "properties": {"info": info},
            "type": "Feature",
        }
        features.append(f)

    return jsonify(features)


@app.route("/map")
def map():
    return render_template("map.html")
