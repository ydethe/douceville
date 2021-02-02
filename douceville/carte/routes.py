import time

from flask import (
    render_template,
    request,flash,
    redirect,
    url_for,
    Markup,
)

from douceville import logger
from douceville.config import Config
from douceville.utils import logged, Serializer
from douceville.carte import carte_bp
from douceville.carte.forms import QueryForm


@carte_bp.route("/query", methods=["GET"])
def recherche():
    form = QueryForm()
    
    if current_user.getCurrentPeriodEnd() < time.time() and not current_user.admin:
        msg = Markup('''Merci d'acheter une licence à partir de <a href="%s">votre page de profil</a>.''' % url_for('users.profile'))
        flash(msg)
        return render_template("carte_query.html", form=form)
        
    if form.validate_on_submit():
        req_param = {}
        req_param["address"] = form.address.data
        req_param["transp"] = form.transp.data
        req_param["dist"] = form.dist.data * 60
        req_param["stat_min"] = form.stat_min.data
        req_param["nature"] = form.nature.data
        req_param["secteur"] = form.secteur.data
        req_param["year"] = "2018"
        req_param["api_key"] = current_user.api_key
        
        logger.debug("carte param : %s" % str(req_param))

        s = Serializer()
        token = s.serialize(req_param)

        return redirect(url_for(".carte", token=token))

    return render_template("carte_query.html", form=form)


@carte_bp.route("/", methods=["GET", "POST"])
def carte():
    token = request.args.get("token", "")

    if token != '':
        s = Serializer()
        dat = s.deserialize(token)

        year = dat.get("year", "2018")
        address = dat.pop("address", "")
        transp = dat.get("transp", "")
        dist = dat.get("dist", "300")
        nature = dat.get("nature", [])
        secteur = dat.get("secteur", [])
        stat_min = dat.get("stat_min", "0")

        if address != "":
            dat["lon"], dat["lat"] = geocodeUserAddress(address)

    # api_url = 
    # api_key = 

    return render_template(
        "carte.html",
        points_request="%s:%i/enseignement?token=%s"
        % (Config.HOST, Config.PORT, token),
        isochrone_request="%s:%i/isochrone?token=%s"
        % (Config.HOST, Config.PORT, token),
    )
