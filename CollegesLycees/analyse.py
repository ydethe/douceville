from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from CollegesLycees.init_db import Lycee


engine = create_engine('sqlite:///lycee.db')
session = sessionmaker()
session.configure(bind=engine)
s = session()

# result = s.query(Lycee).all()
result = s.query(Lycee).filter(Lycee.departement == 31).filter(Lycee.secteur_prive).all()

print(len(result))
# for row in result:
#     print(row.UAI)

