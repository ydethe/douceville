from douceville.models import *


q = db.session.query(Etablissement)
for e in q.all():
    if 'contrat ' in e.secteur:
        e.secteur = 'prive'
    elif 'secteur prive' in e.secteur:
        e.secteur = 'prive'
    
    