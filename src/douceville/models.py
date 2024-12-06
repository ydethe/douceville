import time

from sqlalchemy import (
    ForeignKey,
    String,
    DateTime,
    UniqueConstraint,
    create_engine,
    inspect,
    select,
)
from sqlalchemy.engine import Engine
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
    Session,
    sessionmaker,
)
from geoalchemy2 import Geometry
import stripe
from flask_login import UserMixin

from . import logger


__all__ = ["ImportStatus", "Base", "User", "Resultat", "Etablissement"]


def get_engine() -> Engine:
    from .config import config

    engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=False)
    return engine


def get_db():
    engine = get_engine()
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


class ImportStatus(object):
    OK = 0
    COORD_FROM_ADDRESS = 1
    ETAB_FROM_RESULT = 2


class Base(DeclarativeBase):
    pass


class User(UserMixin, Base):
    __tablename__ = "dvuser"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True)
    login: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(1024), nullable=True, unique=False)
    company: Mapped[str] = mapped_column(String(1024), nullable=True, unique=False)
    location: Mapped[str] = mapped_column(String(1024), nullable=True, unique=False)
    email: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    avatar_url: Mapped[str] = mapped_column(String(1024), nullable=True, unique=False)
    hashed_pwd: Mapped[str] = mapped_column(String(1024), nullable=True)
    admin: Mapped[str] = mapped_column(nullable=False, default=False)
    active: Mapped[str] = mapped_column(nullable=False, default=False)
    stripe_id: Mapped[str] = mapped_column(String(191), nullable=True, unique=True)

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        engine = get_engine()
        with Session(engine) as session:
            stmt = select(cls).where(cls.email == email)
            q = session.scalars(stmt).all()
            if len(q) == 0:
                return None
            else:
                return q[0]

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
        # TODO: solve instance update with sqlalchemy
        # db.session.commit()

        return client["id"]

    def isCorrectPassword(self, plaintext):
        from .app import bcrypt

        return bcrypt.check_password_hash(self.hashed_pwd, plaintext)

    def __repr__(self):
        r = self.asDict()
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Resultat(Base):
    __tablename__ = "resultat"
    __table_args__ = (UniqueConstraint("diplome", "annee", "etablissement_uai"),)

    idx: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    diplome: Mapped[str] = mapped_column(String(191), nullable=False)
    annee: Mapped[int] = mapped_column(nullable=False)
    presents: Mapped[int]
    admis: Mapped[int]
    mentions: Mapped[int]
    etablissement_uai: Mapped[str] = mapped_column(
        String(10), ForeignKey("etablissement.UAI"), nullable=False
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


class Etablissement(Base):
    __tablename__ = "etablissement"

    # Identification
    UAI: Mapped[str] = mapped_column(String(10), primary_key=True, nullable=False)
    nom: Mapped[str] = mapped_column(String(191), nullable=False)
    adresse: Mapped[str] = mapped_column(String(191), nullable=True)
    lieu_dit: Mapped[str] = mapped_column(String(191), nullable=True)
    code_postal: Mapped[str] = mapped_column(String(6), nullable=False)
    commune: Mapped[str] = mapped_column(String(191), nullable=False)
    # https://gist.github.com/joshuapowell/e209a4dac5c8187ea8ce#file-gistfile1-md
    position = mapped_column(Geometry("POINT"), nullable=False)
    # position :Mapped[str]=  mapped_column(String(191), nullable=False)
    departement: Mapped[str] = mapped_column(String(191), nullable=False)
    academie: Mapped[str] = mapped_column(String(191))
    secteur: Mapped[str] = mapped_column(String(191), nullable=False)
    ouverture = mapped_column(DateTime(), nullable=True)
    nature: Mapped[str] = mapped_column(String(191), nullable=False)
    resultats = relationship(
        "Resultat", backref="etablissement", lazy="dynamic", cascade="all, delete"
    )

    def __repr__(self):
        r = self.asDict()
        ks = list(r.keys())
        for k in ks:
            if r[k] is None:
                r.pop(k)
        return str(r)

    def asDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
