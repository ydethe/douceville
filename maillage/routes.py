import os

from sqlalchemy import not_, or_

from flask import render_template
from geojson import Feature, Point, FeatureCollection
import geojson

from maillage.config import basedir
from maillage import app
from maillage.models import Etablissement


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
        .filter(not_(Etablissement.latitude.is_(None))).all()
    )

    l_feat = []
    for e in a:
        info = ""

        stat_brevet = 0
        stat_bac = 0

        info += "Réussite brevet : %i%%" % (100 * stat_brevet)
        info += "\nRéussite bac GT : %i%%" % (100 * stat_bac)

        f = {
            "geometry": {"coordinates": [e.longitude, e.latitude], "type": "Point"},
            "properties": {"nom": e.nom, "info": info},
            "type": "Feature",
        }
        l_feat.append(f)

    feat_coll = FeatureCollection(l_feat)
    js = geojson.dumps(feat_coll)
    # with open(os.path.join(basedir, "static", "toto.geojson"), "w") as f:
    #     f.write(js)

    return render_template("map.html", geojson_data=js)
