from douceville.models import *


for e,r in db.session.query(Etablissement,Resultat).filter(Etablissement.UAI=='0290064M').filter(Etablissement.UAI==Resultat.etablissement_id).all():
    print(r,r.annee)
