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
# result = s.query(Etablissement).filter(Etablissement.departement == 31).filter(Etablissement.secteur_prive).all()
# result = s.query(Etablissement).filter(Etablissement.departement == 31).filter(Etablissement.latitude.is_(None)).all()
# result = s.query(Etablissement).filter(Etablissement.latitude.is_(None)).all()
# result = s.query(Etablissement).filter(Etablissement.UAI == "0010076C").all()

print(len(result))

# for row in result:
#     print(object_as_dict(row))

