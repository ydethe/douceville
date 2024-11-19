from ..models import db, Nature, Resultat, Etablissement


s = db.session

s.query(Nature).delete()
s.query(Resultat).delete()
s.query(Etablissement).delete()

s.commit()
