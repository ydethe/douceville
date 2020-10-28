from sqlalchemy import inspect
from geoalchemy2 import Geometry

from douceville import db


class Resultat(db.Model):
    __tablename__ = "resultat"
    __table_args__ = (db.UniqueConstraint("diplome", "annee", "etablissement_id"),)

    idx = db.Column(db.Integer, primary_key=True, nullable=False)
    diplome = db.Column(db.String(191), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    presents = db.Column(db.Integer, nullable=False)
    admis = db.Column(db.Integer)
    mentions = db.Column(db.Integer)

    etablissement_id = db.Column(
        db.String(10), db.ForeignKey("etablissement.UAI"), nullable=False
    )

    def __repr__(self):
        r = self.asDict()
        r.pop("position", None)
        ks = list(r.keys())
        for k in ks:
            if r[k] is None:
                r.pop(k)
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Etablissement(db.Model):
    __tablename__ = "etablissement"

    # Identification
    UAI = db.Column(db.String(10), primary_key=True)
    nom = db.Column(db.String(191), nullable=False)
    adresse = db.Column(db.String(191))
    lieu_dit = db.Column(db.String(191))
    code_postal = db.Column(db.String(6))
    academie = db.Column(db.String(191))
    nature = db.Column(db.String(191), nullable=False)
    departement = db.Column(db.Integer, nullable=False)
    secteur = db.Column(db.String(191), nullable=False)
    commune = db.Column(db.String(191), nullable=False)
    ouverture = db.Column(db.DateTime())
    # https://gist.github.com/joshuapowell/e209a4dac5c8187ea8ce#file-gistfile1-md
    position = db.Column(Geometry("POINT"))

    resultats = db.relationship("Resultat", backref="etablissement", lazy="dynamic")

    def __repr__(self):
        r = self.asDict()
        r.pop("position", None)
        ks = list(r.keys())
        for k in ks:
            if r[k] is None:
                r.pop(k)
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
