from collections import defaultdict
import logging
import typing as T

from flask import jsonify, request
from flask_login import login_required
from geoalchemy2.shape import to_shape
from sqlalchemy import func, select
from sqlalchemy.orm import Session


from . import enseignement_bp
from ...models import Etablissement, Resultat


def etablissement_info_display(etab: Etablissement, year: int | None) -> T.Tuple[str, float]:
    info = "<b>[%s]%s</b>" % (etab.UAI, etab.nom)

    if year is not None:
        year = int(year)

    stat = 100
    max_year = defaultdict(lambda: -1)
    cres: Resultat
    res: dict = {}
    for cres in etab.resultats:
        if cres.admis is None or cres.presents is None:
            continue

        if cres.annee > max_year[cres.diplome]:
            max_year[cres.diplome] = cres.annee
            res[cres.diplome] = cres.asDict()

        if year is not None and cres.annee == year:
            res[cres.diplome] = cres.asDict()
            break

    for diplome in res.keys():
        res_diplome = res[diplome]
        stat = int(100 * res_diplome["admis"] / res_diplome["presents"])
        info_res = "<br>Réussite %s %i : %i%%" % (diplome, res_diplome["annee"], stat)
        info += info_res

    return info, stat


@enseignement_bp.route("/", methods=["GET"])
@login_required
def enseignement():
    from ...models import Etablissement, get_engine
    from ...utils import Serializer
    from ...blueprints.isochrone.geographique import calcIsochrone

    logger = logging.getLogger("douceville_logger")
    token = request.args.get("token", "")
    if token == "":
        return jsonify({})

    s = Serializer()
    dat = s.deserialize(token)
    logger.debug("enseignement param : %s" % str(dat))

    year = dat.get("year", None)
    lat = dat.get("lat", 1.39396)
    lon = dat.get("lon", 43.547864)
    dist = dat.get("dist", 600)
    transp = dat.get("transp", "")
    nature = dat.get("nature", [])
    secteur = dat.get("secteur", [])
    stat_min = dat.get("stat_min", 0)

    center = [lon, lat]
    iso = calcIsochrone(center, dist, transp)

    stmt = select(Etablissement).where(func.ST_Within(Etablissement.position, iso.getGeom()))

    if nature != []:
        stmt = stmt.where(Etablissement.nature.in_(nature))

    if secteur != []:
        stmt = stmt.where(Etablissement.secteur.in_(secteur))

    engine = get_engine()
    with Session(engine) as session:
        a = session.scalars(stmt)

        features = []
        for e in a.all():
            info, stat = etablissement_info_display(e, year=year)

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
