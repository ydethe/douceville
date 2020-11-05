from sqlalchemy import create_engine, inspect, or_
from sqlalchemy.orm import sessionmaker

from douceville.models import *
from douceville.config import Config


s = db.session

s.query(Nature).delete()
s.query(Resultat).delete()
s.query(Etablissement).delete()

s.commit()
