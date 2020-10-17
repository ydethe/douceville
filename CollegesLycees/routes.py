import os

from sqlalchemy import not_, or_

from flask import render_template
from geojson import Feature, Point, FeatureCollection
import geojson

from CollegesLycees.config import basedir
from CollegesLycees import app
from CollegesLycees.models import Etablissement


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    return render_template("index.html", title="Home", user=user)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/map")
def map():
    a = (
        Etablissement.query
        # .filter(Etablissement.departement == 31)
        .filter(not_(Etablissement.latitude.is_(None)))
        .all()
    )

    l_feat = []
    for e in a:
        info = ""

        if e.admis_brevet is None or e.presents_brevet is None:
            stat_brevet = None
        else:
            stat_brevet = e.admis_brevet / e.presents_brevet
            info += "Réussite brevet : %i%%" % (100 * stat_brevet)
            if stat_brevet < 0.98:
                continue

        if e.presents_gt is None:
            stat_bac = None
        elif not e.mentions_gt is None:
            stat_bac = e.mentions_gt / e.presents_gt
            info += "\nRéussite bac GT : %i%%" % (100 * stat_bac)
            if stat_bac < 0.98:
                continue
        elif not e.admis_gt is None:
            stat_bac = e.admis_gt / e.presents_gt
            info += "\nRéussite bac GT : %i%%" % (100 * stat_bac)
            if stat_bac < 0.98:
                continue

        if stat_brevet is None and stat_bac is None:
            continue

        f = {
            "geometry": {"coordinates": [e.longitude, e.latitude], "type": "Point"},
            "properties": {"nom": e.nom, "info": info},
            "type": "Feature",
        }
        l_feat.append(f)

    feat_coll = FeatureCollection(l_feat)
    js = geojson.dumps(feat_coll)
    with open(os.path.join(basedir, "static", "toto.geojson"), "w") as f:
        f.write(js)
    return render_template("map.html", geojson_file="static/toto.geojson")
