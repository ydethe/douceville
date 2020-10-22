from sqlalchemy import not_

from flask import render_template, jsonify

from maillage.config import Config
from maillage import app
from maillage.models import Etablissement, Resultat


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    return render_template("index.html", title="Home", user=user)


@app.route("/points", methods=["GET"])
def get_all_points():
    a = (
        Etablissement.query
        # .filter(Etablissement.departement == 31)
        .filter(not_(Etablissement.latitude.is_(None)))
        .all()
    )

    features = []
    for e in a:
        info = "<b>%s</b>" % e.nom

        results = (
            Resultat.query.filter(Resultat.etablissement_id == e.UAI)
            .filter(Resultat.annee == 2018)
            .all()
        )
        for res in results:
            if not res.admis is None:
                stat = res.admis / res.presents
                if stat > 1 or stat < 0.3:
                    print(res)
                info += "<br>Réussite %s : %i%%" % (res.diplome, 100 * stat)

        f = {
            "geometry": {"coordinates": [e.longitude, e.latitude], "type": "Point"},
            "properties": {"info": info},
            "type": "Feature",
        }
        features.append(f)

    return jsonify(features)


@app.route("/map")
def map():
    return render_template(
        "map.html", points_request="%s:%i/points" % (Config.HOST, Config.PORT)
    )
