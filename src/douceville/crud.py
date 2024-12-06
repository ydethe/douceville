from sqlalchemy.orm import Session
from sqlalchemy import select

from .schemas import GithubUser, DvUser, Etablissement


def get_user_by_login(db: Session, github_login: str) -> DvUser:
    stmt = select(DvUser).where(DvUser.login == github_login)

    a = list(db.scalars(stmt))
    if len(a) == 0:
        return None
    else:
        return a[0]


def create_user(db: Session, github_user: GithubUser) -> DvUser:
    new_user = DvUser(
        login=github_user.login,
        name=github_user.name,
        company=github_user.company,
        location=github_user.location,
        email=github_user.email,
        avatar_url=github_user.avatar_url,
        admin=False,
        active=False,
    )
    db.add_all([new_user])
    db.commit()
    return new_user


def get_user(db: Session, user_id: int) -> DvUser:
    stmt = select(DvUser).where(DvUser.id == user_id)

    a = list(db.scalars(stmt))
    if len(a) == 0:
        return None
    else:
        return a[0]


def get_etab(db: Session, etab_id: int) -> Etablissement:
    stmt = select(Etablissement).where(Etablissement.id == etab_id)

    a = list(db.scalars(stmt))
    if len(a) == 0:
        return None
    else:
        return a[0]
