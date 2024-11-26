from ..models import db, Etablissement, ImportStatus

# from ..blueprints.isochrone.geographique import findCoordFromAddress


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
        if k not in ed.keys() or ed[k] is None:
            print("   %s" % k)
