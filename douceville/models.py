from sqlalchemy import inspect, event
from geoalchemy2 import Geometry

from douceville import db


class ImportStatus(object):
    OK = 0
    COORD_FROM_ADDRESS = 1
    ETAB_FROM_RESULT = 2

class Nature(db.Model):
    __tablename__ = "nature"
    __table_args__ = (db.UniqueConstraint("nature", "etablissement_id"),)

    idx = db.Column(db.Integer, primary_key=True, nullable=False)
    nature = db.Column(db.String(191), nullable=False)

    etablissement_id = db.Column(
        db.String(10), db.ForeignKey("etablissement.UAI"), nullable=False
    )

    def __repr__(self):
        r = self.asDict()
        r.pop("position", None)
        r.pop("idx", None)
        ks = list(r.keys())
        for k in ks:
            if r[k] is None:
                r.pop(k)
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Resultat(db.Model):
    __tablename__ = "resultat"
    __table_args__ = (db.UniqueConstraint("diplome", "annee", "etablissement_id"),)

    idx = db.Column(db.Integer, primary_key=True, nullable=False)
    diplome = db.Column(db.String(191), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    presents = db.Column(db.Integer)
    admis = db.Column(db.Integer)
    mentions = db.Column(db.Integer)

    etablissement_id = db.Column(
        db.String(10), db.ForeignKey("etablissement.UAI"), nullable=False
    )

    def __repr__(self):
        r = self.asDict()
        r.pop("position", None)
        r.pop("idx", None)
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
    UAI = db.Column(db.String(10), primary_key=True, nullable=False)
    nom = db.Column(db.String(191), nullable=False)
    adresse = db.Column(db.String(191))
    lieu_dit = db.Column(db.String(191))
    code_postal = db.Column(db.String(6), nullable=False)
    commune = db.Column(db.String(191), nullable=False)
    position = db.Column(Geometry("POINT"), nullable=False)
    # position = db.Column(db.String(191), nullable=False)
    departement = db.Column(db.Integer, nullable=False)
    academie = db.Column(db.String(191), nullable=False)
    secteur = db.Column(db.String(191), nullable=False)
    ouverture = db.Column(db.DateTime())
    import_status = db.Column(db.Integer, nullable=False)
    # https://gist.github.com/joshuapowell/e209a4dac5c8187ea8ce#file-gistfile1-md
    
    resultats = db.relationship("Resultat", backref="etablissement", lazy="dynamic")
    natures = db.relationship("Nature", backref="etablissement", lazy="dynamic")

    def __repr__(self):
        r = self.asDict()
        ks = list(r.keys())
        for k in ks:
            if r[k] is None:
                r.pop(k)
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
