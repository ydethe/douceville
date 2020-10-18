from sqlalchemy import inspect

from CollegesLycees import db


# Diplomes :
# - brevet

# FILIERE GENERALE
# - bac s
# - bac l
# - bac es

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

res_etab = db.Table(
    "res_etab",
    db.Column(
        "etablissement_idx",
        db.String,
        db.ForeignKey("etablissement.UAI"),
        primary_key=True,
    ),
    db.Column(
        "resultat_idx", db.Integer, db.ForeignKey("resultat.idx"), primary_key=True
    ),
)

acces_etab = db.Table(
    "acces_etab",
    db.Column(
        "etablissement_idx",
        db.String,
        db.ForeignKey("etablissement.UAI"),
        primary_key=True,
    ),
    db.Column("acces_idx", db.Integer, db.ForeignKey("acces.idx"), primary_key=True),
)


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


class Resultat(db.Model):
    __tablename__ = "resultat"

    idx = db.Column(db.Integer, primary_key=True, nullable=False)
    diplome = db.Column(db.String, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    presents = db.Column(db.Integer, nullable=False)
    admis = db.Column(db.Integer, nullable=False)
    mentions = db.Column(db.Integer)


class Etablissement(db.Model):
    __tablename__ = "etablissement"

    # Identification
    UAI = db.Column(db.String, primary_key=True)
    nom = db.Column(db.String, nullable=False)
    academie = db.Column(db.String, nullable=False)
    departement = db.Column(db.Integer, nullable=False)
    secteur = db.Column(db.String, nullable=False)
    commune = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    resultats = db.relationship("Resultat", secondary=res_etab)
    acces = db.relationship("Acces", secondary=acces_etab)

    def __repr__(self):
        return "<Etablissement {}, lat={}>".format(self.nom, self.latitude)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
