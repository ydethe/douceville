from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField as DVSelField
from wtforms.fields import SelectField
from wtforms.fields import StringField, SubmitField, FloatField
from sqlalchemy import distinct


def buildList(attr):
    from ...models import db

    elem = [str(x[0]) for x in db.session.query(distinct(attr)).all()]
    elem.sort()

    ret_list = [(str(x), str(x)) for x in elem]

    return ret_list


class QueryForm(FlaskForm):
    from ...models import db, Etablissement

    address = StringField("Adresse")
    transp = SelectField(
        "Transport", choices=[("driving-car", "Voiture"), ("cycling-road", "Vélo")]
    )
    dist = FloatField("Temps (min)")
    stat_min = FloatField("stat_min")
    nature = DVSelField("Nature", choices=["Collège", "Lycée"])
    secteur = DVSelField("Secteur", choices=buildList(Etablissement.secteur))

    submit = SubmitField("Chercher")
