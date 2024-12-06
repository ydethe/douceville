from getpass import getpass

from sqlalchemy.orm import Session
from flask_mail import Message
import typer


tapp = typer.Typer()


@tapp.command()
def add_user(
    login: str = typer.Argument(None, help="Github login"),
    email: str = typer.Argument(None, help="Email"),
    pwd: str = typer.Argument(None, help="Password"),
    admin: bool = typer.Option(False, help="Falg to grant the user admin privilege"),
    active: bool = typer.Option(False, help="Flag to make the user active"),
):
    """Register a user in the base"""
    # logger = logging.getLogger("douceville_logger")
    from ...schemas import DvUser, get_engine
    from ...app import app, bcrypt, mail
    from ...config import config
    from ...utils import Serializer

    if email is None:
        email = input("email: ")
    if pwd is None:
        pwd = getpass("password: ")

    q = DvUser.get_by_email(email)
    if q is not None:
        return

    hpwd = bcrypt.generate_password_hash(pwd, config.BCRYPT_ROUNDS)
    user = DvUser(login=login, email=email, hashed_pwd=hpwd.decode(), admin=admin, active=active)

    if not active:
        s = Serializer()
        token = s.serialize({"email": email})
        with app.app_context():
            msg = Message("Hello", recipients=[email])
            msg.html = f'<a href="/users/confirm?token={token}">Click here to confirm</a>'
            mail.send(msg)

    engine = get_engine()
    with Session(engine) as session:
        session.add_all([user])
        session.commit()


def add_user_main():
    tapp()
