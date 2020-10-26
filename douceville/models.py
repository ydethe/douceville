from sqlalchemy import inspect
from geoalchemy2 import Geometry

from douceville import db


# Diplomes :
# - brevet

# FILIERE GENERALE
# - bac_general

# FILIERE TECHNOLOGIQUE
# - stmg
# - stl
# - st2s
# - sti2d
# - std2a
# - tmd
# - sthr

# FILIERE PRO
# - production
# - services
# - spe_pluritech
# - transformations
# - genie_civil
# - materiaux_souples
# - meca_elec
# - spe_plurivalentes
# - echanges_gestion
# - communication_info
# - services_personnes
# - services_collectivite


class Acces(db.Model):
    __tablename__ = "acces"

    # Identification
    idx = db.Column(db.Integer, primary_key=True, nullable=False)

    # Filiere generale et techno
    taux_2nde_gt_bac = db.Column(db.Integer)
    taux_1ere_gt_bac = db.Column(db.Integer)
    taux_term_gt_bac = db.Column(db.Integer)

    # Filiere pro
    taux_2nde_pro_bac = db.Column(db.Integer)
    taux_1ere_pro_bac = db.Column(db.Integer)
    taux_term_pro_bac = db.Column(db.Integer)

    etablissement_id = db.Column(
        db.String(10), db.ForeignKey("etablissement.UAI"), nullable=False
    )

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


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
    academie = db.Column(db.String(191), nullable=False)
    nature = db.Column(db.String(191), nullable=False)
    departement = db.Column(db.Integer, nullable=False)
    secteur = db.Column(db.String(191), nullable=False)
    commune = db.Column(db.String(191), nullable=False)
    ouverture = db.Column(db.DateTime())
    # https://gist.github.com/joshuapowell/e209a4dac5c8187ea8ce#file-gistfile1-md
    # latitude = db.Column(db.Float, nullable=False)
    # longitude = db.Column(db.Float, nullable=False)
    position = db.Column(Geometry('POINT'))

    def __repr__(self):
        return "<Etablissement {}, lat={}>".format(self.nom, self.latitude)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
