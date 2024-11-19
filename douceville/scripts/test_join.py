from ..models import db, Etablissement


# uai = '0010005A' # 1 resultat
uai = "0010022U"  # 2 resultats

e = db.session.query(Etablissement).filter(Etablissement.UAI == uai).first()
print(e)

for r in e.resultats:
    print("   ", r)
