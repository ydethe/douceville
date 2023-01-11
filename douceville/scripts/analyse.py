from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect

from douceville.models import *
from douceville.config import Config

# from douceville.blueprints.isochrone.geographique import findCoordFromAddress


s = db.session

result = s.query(Etablissement).filter(Etablissement.import_status == ImportStatus.ETAB_FROM_RESULT)
# print("%i enregistrements" % result.count())

l_keys = [
    "UAI",
    "nom",
    "adresse",
    "lieu_dit",
    "code_postal",
    "commune",
    "position",
    "departement",
    "academie",
    "secteur",
    "ouverture",
    "import_status",
]
for e in result.all():
    ed = e.asDict()
    for k in l_keys:
        if k == "UAI":
            print(ed[k])
        if not k in ed.keys() or ed[k] is None:
            print("   %s" % k)

# result = s.query(Nature).filter(Nature.etablissement_id=='0010005A')
# print(result.all())

# result = s.query(Nature).filter(Nature.nature == '')
# print(result.count())
# print(result.all())

# print(bulidList(Nature.nature))
