from sqlalchemy import not_, distinct
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from flask import render_template, jsonify, make_response

from douceville.config import Config
from douceville import app
from douceville.models import db, Etablissement, Resultat
from douceville.isochrone import calcIsochrone


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Yann"}
    r = db.session.query(distinct(Etablissement.nature)).all()

    return render_template(
        "index.html", title="Home", user=user, natures=[x[0] for x in r]
    )


@app.route(
    "/points/<int:year>/<nature>/<int:departement>/<int:stat_min>", methods=["GET"]
)
def get_all_points(year, nature, departement, stat_min):
    dist = 500
    center = [1.39396,43.547864]
    iso = calcIsochrone(center, dist)

    pts = iso['features'][0]['geometry']['coordinates'][0]

    pg = 'POLYGON(('
    for lon,lat in pts:
        pg += '%f %f,' % (lon,lat)
    pg = pg[:-1] + '))'

    a = Etablissement.query.filter(not_(Etablissement.position.is_(None))).filter(func.ST_Within(Etablissement.position, func.ST_GeomFromEWKT(pg)))


    if departement > 0:
        a = a.filter(Etablissement.departement == departement)

    if nature != "0":
        a = a.filter(Etablissement.nature == nature)

    features = []
    for e in a.all():
        print(to_shape(e.position))

        info = "<b>[%s]%s</b>" % (e.UAI, e.nom)

        results = (
            Resultat.query.filter(Resultat.etablissement_id == e.UAI)
            .filter(Resultat.annee == year)
            .all()
        )

        stat = 0
        for res in results:
            if not res.admis is None:
                stat = int(100 * res.admis / res.presents)
                info += "<br>Réussite %s : %i%%" % (res.diplome, stat)

        if stat >= stat_min:
            p = to_shape(e.position)
            lon,lat = p.coords.xy
            f = {
                "geometry": {"coordinates": [lon[0], lat[0]], "type": "Point"},
                "properties": {"info": info},
                "type": "Feature",
            }
            features.append(f)

    return jsonify(features)


@app.route("/map/<int:year>/<nature>", methods=["GET"])
@app.route("/map/<int:year>/<nature>/<int:departement>", methods=["GET"])
@app.route("/map/<int:year>/<nature>/<int:departement>/<int:stat_min>")
def map(year, nature, departement=0, stat_min=0):
    dist = 20 * 60
    center = [1.387276, 43.545640]
    iso = calcIsochrone(center, dist)

    return render_template(
        "map.html",
        isochrone=iso["features"],
        points_request="%s:%i/points/%i/%s/%i/%i"
        % (Config.HOST, Config.PORT, year, nature, departement, stat_min),
    )
