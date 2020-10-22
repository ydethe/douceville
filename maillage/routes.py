from sqlalchemy import not_, distinct

from flask import render_template, jsonify

from maillage.config import Config
from maillage import app
from maillage.models import db, Etablissement, Resultat


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    r = db.session.query(distinct(Etablissement.nature)).all()

    return render_template("index.html", title="Home", user=user, natures=[x[0] for x in r])


@app.route("/points/<int:year>/<nature>/<int:departement>/<int:stat_min>", methods=["GET"])
def get_all_points(year, nature, departement, stat_min):
    a = (
        Etablissement.query
        .filter(Etablissement.departement == departement)
        .filter(Etablissement.nature == nature)
        .filter(not_(Etablissement.latitude.is_(None)))
        .all()
    )

    features = []
    for e in a:
        info = "<b>%s</b>" % e.nom

        results = (
            Resultat.query.filter(Resultat.etablissement_id == e.UAI)
            .filter(Resultat.annee == year)
            .all()
        )

        stat = 0
        for res in results:
            if not res.admis is None:
                stat = int(100*res.admis / res.presents)
                info += "<br>Réussite %s : %i%%" % (res.diplome, stat)

        if stat >= stat_min:
            f = {
                "geometry": {"coordinates": [e.longitude, e.latitude], "type": "Point"},
                "properties": {"info": info},
                "type": "Feature",
            }
            features.append(f)

    return jsonify(features)


@app.route("/map/<int:year>/<nature>/<int:departement>/<int:stat_min>")
def map(year, nature, departement, stat_min):
    return render_template(
        "map.html", points_request="%s:%i/points/%i/%s/%i/%i" % (Config.HOST, Config.PORT, year, nature, departement, stat_min)
    )
