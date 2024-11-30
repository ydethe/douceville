from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField as DVSelField
from wtforms.fields import SelectField
from wtforms.fields import StringField, SubmitField, FloatField
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm import Session
from sqlalchemy import select


def buildList(attr: InstrumentedAttribute):
    # TODO: solve this query
    from ...models import get_engine

    engine = get_engine()
    with Session(engine) as session:
        elem = list(session.scalars(select(attr).distinct()))
    elem.sort()

    ret_list = [(str(x), str(x)) for x in elem]

    return ret_list


class QueryForm(FlaskForm):
    from ...models import Etablissement

    address = StringField("Adresse")
    transp = SelectField(
        "Transport", choices=[("driving-car", "Voiture"), ("cycling-road", "Vélo")]
    )
    dist = FloatField("Temps (min)")
    stat_min = FloatField("stat_min")
    nature = DVSelField("Nature", choices=["Collège", "Lycée"])
    secteur = DVSelField("Secteur", choices=buildList(Etablissement.secteur))

    submit = SubmitField("Chercher")
