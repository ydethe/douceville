from douceville.models import *
from douceville.blueprints.carte.forms import buildList


def check():
    for x,_ in buildList(Etablissement.secteur):
        print(x)
    print(72*'-')

check()

q = db.session.query(Etablissement)
for e in q.all():
    if 'contrat ' in e.secteur:
        e.secteur = 'prive'
    elif 'c0ntrat ' in e.secteur:
        e.secteur = 'prive'
    elif 'secteur prive' in e.secteur:
        e.secteur = 'prive'
    
db.session.commit()

check()

