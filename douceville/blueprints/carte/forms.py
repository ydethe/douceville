from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField as DVSelField
from wtforms.fields import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

from sqlalchemy import distinct
from douceville.models import db, Nature, Etablissement


def buildList(attr):
    elem = [str(x[0]) for x in db.session.query(distinct(attr)).all()]
    elem.sort()

    l = [(str(x), str(x)) for x in elem]

    return l


class QueryForm(FlaskForm):
    address = StringField("address")
    dist = FloatField("dist")
    stat_min = FloatField("stat_min")
    nature = DVSelField("nature", choices=buildList(Nature.nature))
    secteur = DVSelField("secteur", choices=buildList(Etablissement.secteur))

    submit = SubmitField("Chercher")
