from sqlalchemy.orm import Session
from sqlalchemy import select

from .schemas import GithubUser
from .models import User as DbUser


def get_user_by_login(db: Session, github_login: str) -> DbUser:
    stmt = select(DbUser).where(DbUser.login == github_login)

    a = db.scalars(stmt)
    if a.count() == 0:
        return None
    else:
        return a.first()


def create_user(db: Session, github_user: GithubUser) -> DbUser:
    new_user = DbUser(
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


def get_user(db: Session, user_id: int) -> DbUser:
    stmt = select(DbUser).where(DbUser.id == user_id)

    a = db.scalars(stmt)
    if a.count() == 0:
        return None
    else:
        return a.first()
