from ..models import db, Resultat, Etablissement


s = db.session

s.query(Resultat).delete()
s.query(Etablissement).delete()

s.commit()
