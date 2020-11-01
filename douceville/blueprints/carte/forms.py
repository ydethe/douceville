from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField as DVSelField
from wtforms.fields import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

from sqlalchemy import distinct
from douceville.models import db, Etablissement


def buildList(attr):
    a = getattr(Etablissement, attr)
    elem = [str(x[0]) for x in db.session.query(distinct(a)).all()]
    elem.sort()

    l = [("all", "all")] + [(str(x), str(x)) for x in elem]

    return l


class QueryForm(FlaskForm):
    address = StringField("address")
    dist = FloatField("dist")
    stat_min = FloatField("stat_min")
    nature = DVSelField(u"nature", choices=buildList("nature"))
    secteur = DVSelField(u"secteur", choices=buildList("secteur"))

    submit = SubmitField("Chercher")
