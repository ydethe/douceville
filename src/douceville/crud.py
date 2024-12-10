from sqlalchemy.orm import Session
from sqlalchemy import select

from .schemas import Etablissement


def get_etab(db: Session, uai: str) -> Etablissement:
    stmt = select(Etablissement).where(Etablissement.UAI == uai)

    a = list(db.scalars(stmt))
    if len(a) == 0:
        return None
    else:
        return a[0]
