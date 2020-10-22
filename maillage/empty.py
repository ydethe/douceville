from sqlalchemy import create_engine, inspect, or_
from sqlalchemy.orm import sessionmaker

from maillage.models import Etablissement, Resultat
from maillage.config import Config


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

session = sessionmaker()
session.configure(bind=engine)
s = session()

s.query(Resultat).delete()
s.query(Etablissement).delete()

s.commit()
