from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from init_db import Lycee


engine = create_engine('sqlite:///lycee_gt_pro.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()

# result = s.query(Lycee).all()
# result = s.query(Lycee).filter(Lycee.departement == 31).filter(Lycee.secteur_prive).all()
result = s.query(Lycee).filter(Lycee.departement == 31).filter(Lycee.latitude.is_(None)).all()

print(len(result))
for row in result:
    print(row.nom)

