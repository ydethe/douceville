import time

from sqlalchemy import inspect
from geoalchemy2 import Geometry
import stripe
from flask_login import UserMixin

from .app import db, bcrypt
from . import logger


__all__ = ["User", "Resultat", "Etablissement"]


class ImportStatus(object):
    OK = 0
    COORD_FROM_ADDRESS = 1
    ETAB_FROM_RESULT = 2


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.BigInteger, nullable=False, primary_key=True)
    email = db.Column(db.String(1024), nullable=False, unique=True)
    hashed_pwd = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    stripe_id = db.Column(db.String(191), unique=True)

    def getCurrentPeriodEnd(self):
        sid = self.getStripeID()

        subscriptions = stripe.Subscription.list(
            customer=sid, status="active", current_period_end={"gt": int(time.time())}
        )
        if len(subscriptions["data"]) == 0:
            t = -1
        else:
            s = subscriptions["data"][0]
            t = s["current_period_end"]

        return t

    def getStripeID(self):
        if self.stripe_id is not None:
            return self.stripe_id

        ret = stripe.Customer.list(email=self.email)
        if len(ret) == 0:
            client = stripe.Customer.create(
                email=self.email,
                metadata={"dv_id": self.id},
            )
        elif len(ret) == 1:
            client = ret["data"][0]
        else:
            logger.error("Too much clients in stripe API")
            return None

        self.stripe_id = client["id"]
        db.session.commit()

        return client["id"]

    def isCorrectPassword(self, plaintext):
        return bcrypt.check_password_hash(self.hashed_pwd, plaintext)

    def __repr__(self):
        r = self.asDict()
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Resultat(db.Model):
    __tablename__ = "resultat"
    __table_args__ = (db.UniqueConstraint("diplome", "annee", "etablissement_uai"),)

    idx = db.Column(db.Integer, primary_key=True, nullable=False)
    diplome = db.Column(db.String(191), nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    presents = db.Column(db.Integer)
    admis = db.Column(db.Integer)
    mentions = db.Column(db.Integer)
    etablissement_uai = db.Column(db.String(10), db.ForeignKey("etablissement.UAI"), nullable=False)

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
    # https://gist.github.com/joshuapowell/e209a4dac5c8187ea8ce#file-gistfile1-md
    position = db.Column(Geometry("POINT"), nullable=False)
    # position = db.Column(db.String(191), nullable=False)
    departement = db.Column(db.Integer, nullable=False)
    academie = db.Column(db.String(191))
    secteur = db.Column(db.String(191), nullable=False)
    ouverture = db.Column(db.DateTime())
    import_status = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.String(191), nullable=False)
    resultats = db.relationship("Resultat", backref="etablissement", lazy="dynamic")

    def __repr__(self):
        r = self.asDict()
        ks = list(r.keys())
        for k in ks:
            if r[k] is None:
                r.pop(k)
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
