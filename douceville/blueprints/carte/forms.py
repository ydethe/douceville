from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField as DVSelField
from wtforms.fields import SelectField
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
    address = StringField("Adresse")
    transp = SelectField(
        "Transport", choices=[("driving-car", "Voiture"), ("cycling-road", "Vélo")]
    )
    dist = FloatField("Temps (min)")
    stat_min = FloatField("stat_min")
    nature = DVSelField("Nature", choices=buildList(Nature.nature))
    secteur = DVSelField("Secteur", choices=buildList(Etablissement.secteur))

    submit = SubmitField("Chercher")
