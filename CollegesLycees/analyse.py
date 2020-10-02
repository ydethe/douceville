from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect

from init_db import Etablissement


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

engine = create_engine('sqlite:///etablissements.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()


result = s.query(Etablissement).all()
print("%i enregistrements" % len(result))

result = s.query(Etablissement).filter(Etablissement.latitude.is_(None)).all()
print("%i enregistrements sans geoloc" % len(result))

result = s.query(Etablissement).filter(Etablissement.departement == 31).filter(Etablissement.latitude.is_(None)).all()
print("%i enregistrements sans geoloc dans le 31" % len(result))

result = s.query(Etablissement).filter(Etablissement.UAI == '0310001H').all()
for row in result:
    print(object_as_dict(row))
    exit(0)
