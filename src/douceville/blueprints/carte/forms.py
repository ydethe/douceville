import typing as T

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

    list_nature: T.List[str] = buildList(Etablissement.nature)
    list_secteur: T.List[str] = buildList(Etablissement.secteur)

    address = StringField("Adresse")
    transp = SelectField(
        "Transport",
        choices=[
            ("foot-walking", "A pied"),
            ("driving-car", "Voiture"),
            ("cycling-road", "Vélo"),
        ],
        default="driving-car",
    )
    dist = FloatField("Temps (min)")
    stat_min = FloatField("Taux de réussite (%)")
    nature = DVSelField("Nature", choices=list_nature)
    secteur = DVSelField("Secteur", choices=[(x, y.title()) for (x, y) in list_secteur])

    submit = SubmitField("Chercher")
