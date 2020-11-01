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
        req_param["nature"] = form.nature.data
        req_param["secteur"] = form.secteur.data
        req_param["year"] = '2018'
        
        s = Serializer()
        token = s.serialize(req_param)

        return redirect(url_for(".carte", token=token))

    return render_template("carte/carte_query.html", form=form)


@carte_bp.route("/", methods=["GET"])
def carte():
    token = request.args.get("token", "")

    s = Serializer()
    dat = s.deserialize(token)
    
    year = dat.get("year", "2018")
    address = dat.pop("address", "")
    dist = dat.get("dist", "300")
    nature = dat.get("nature", [])
    secteur = dat.get("secteur", [])
    stat_min = dat.get("stat_min", "0")
    
    if address != "":
        dat['lon'], dat['lat'] = findCoordFromAddress(address)

    token = s.serialize(dat)

    return render_template(
        "carte/carte.html",
        points_request="%s:%i/enseignement?token=%s"
        % (Config.HOST, Config.PORT, token),
        isochrone_request="%s:%i/isochrone?token=%s"
        % (Config.HOST, Config.PORT, token),
    )
