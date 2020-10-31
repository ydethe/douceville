from flask import (
    Blueprint,
    render_template,
    jsonify,
    make_response,
    request,
    abort,
    flash,
    redirect,
    url_for,
)
from jinja2 import TemplateNotFound
from sqlalchemy import not_, distinct
from geoalchemy2.shape import to_shape
from geoalchemy2 import func

from douceville.config import Config
from douceville.models import db, Etablissement, Resultat
from douceville.utils import logged, Serializer
from douceville.blueprints.carte import carte_bp
from douceville.blueprints.carte.forms import QueryForm
from douceville.blueprints.isochrone.geographique import findCoordFromAddress


@carte_bp.route("/query", methods=["GET", "POST"])
def recherche():
    form = QueryForm()
    if form.validate_on_submit():
        req_param = {}
        req_param["address"] = form.address.data
        req_param["dist"] = form.dist.data
        req_param["stat_min"] = form.stat_min.data
        req_param["academie"] = form.academie.data
        req_param["nature"] = form.nature.data
        req_param["departement"] = form.departement.data
        req_param["secteur"] = form.secteur.data
        req_param["year"] = '2018'
        
        return redirect(url_for(".carte", **req_param))

    return render_template("carte/carte_query.html", form=form)


@carte_bp.route("/", methods=["GET"])
def carte():
    year = request.args.get("year", "2018")
    address = request.args.get("address", "")
    dist = request.args.get("dist", "300")
    academie = request.args.get("academie", "all")
    nature = request.args.get("nature", "all")
    departement = request.args.get("departement", "all")
    secteur = request.args.get("secteur", "all")
    stat_min = request.args.get("stat_min", "0")
    
    if address != "":
        lon, lat = findCoordFromAddress(address)

    s = Serializer()
    dat = {
        "year": year,
        "lon": lon,
        "lat": lat,
        "dist": dist,
        "academie": academie,
        "nature": nature,
        "departement": departement,
        "secteur": secteur,
        "stat_min": stat_min,
    }
    token = s.serialize(dat)

    return render_template(
        "carte/carte.html",
        points_request="%s:%i/enseignement?token=%s"
        % (Config.HOST, Config.PORT, token),
        isochrone_request="%s:%i/isochrone?token=%s"
        % (Config.HOST, Config.PORT, token),
    )
