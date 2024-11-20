from getpass import getpass

from flask_mail import Message
import typer


tapp = typer.Typer()


@tapp.command()
def add_user(
    email: str = typer.Argument(None, help="Email"),
    pwd: str = typer.Argument(None, help="Password"),
    admin: bool = typer.Option(False, help="Falg to grant the user admin privilege"),
    active: bool = typer.Option(False, help="Flag to make the user active"),
):
    """Register a user in the base"""
    # logger = logging.getLogger("douceville_logger")
    from ...models import db, User
    from ...app import app, bcrypt, mail
    from ...config import config
    from ...utils import Serializer

    if email is None:
        email = input("email: ")
    if pwd is None:
        pwd = getpass("password: ")

    q = User.query.filter_by(email=email)
    if q.count() == 0:
        hpwd = bcrypt.generate_password_hash(pwd, config.BCRYPT_ROUNDS)
        user = User(email=email, hashed_pwd=hpwd.decode(), admin=admin, active=active)

        if not active:
            s = Serializer()
            token = s.serialize({"email": email})
            with app.app_context():
                msg = Message("Hello", recipients=[email])
                msg.html = '<a href="%s:%s/users/confirm?token=%s">Click here to confirm</a>' % (
                    config.HOST,
                    config.PORT,
                    token,
                )
                mail.send(msg)

        db.session.add(user)
        db.session.commit()
        print("OK")
    else:
        print("!!! NOK !!!")


def add_user_main():
    tapp()
