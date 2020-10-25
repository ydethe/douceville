from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from geoalchemy2.shape import to_shape

from douceville.models import Etablissement
from douceville.config import Config


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
session = sessionmaker()
session.configure(bind=engine)
s = session()


result = s.query(Etablissement)
print("%i enregistrements" % result.count())

result = s.query(Etablissement).filter(Etablissement.position.is_(None))
print("%i enregistrements sans geoloc" % result.count())

result = (
    s.query(Etablissement)
    .filter(Etablissement.departement == 31)
    .filter(Etablissement.position.is_(None))
)
print("%i enregistrements sans geoloc dans le 31" % result.count())

for row in result:
    print("%s, %s, %s" % (row.UAI, row.commune, row.nom))

result = s.query(Etablissement).filter(Etablissement.departement == 31)
print("%i enregistrements dans le 31" % result.count())

r = result[0]
a = to_shape(r.position)
print(r.UAI, r.nom, a.x, a.y)
