from getpass import getpass
import argparse

from flask_mail import Message

import douceville
from douceville.models import *
from douceville import app, bcrypt, mail
from douceville.config import Config
from douceville.utils import logged, Serializer


def add_user(email=None, pwd=None, admin=False, active=False):
    if email is None:
        email = input("email: ")
    if pwd is None:
        pwd = getpass("password: ")

    q = User.query.filter_by(email=email)
    if q.count() == 0:
        hpwd = bcrypt.generate_password_hash(pwd, Config.BCRYPT_ROUNDS)
        user = User(
            email=email, hashed_pwd=hpwd.decode(), admin=admin, is_active=active
        )

        if not active:
            s = Serializer()
            token = s.serialize({"email": email})
            with app.app_context():
                msg = Message("Hello", recipients=[email])
                msg.html = (
                    '<a href="%s:%s/users/confirm?token=%s">Click here to confirm</a>'
                    % (
                        Config.HOST,
                        Config.PORT,
                        token,
                    )
                )
                mail.send(msg)

        db.session.add(user)
        db.session.commit()
        return True
    else:
        return False


@logged
def main(logger=None):
    logger.info("Maillage, version %s" % douceville.__version__)

    parser = argparse.ArgumentParser(
        description="Maillage France - Gestion utilisateurs"
    )
    parser.add_argument("action", help="action", type=str)
    parser.add_argument("email", help="email", type=str, default=None)
    parser.add_argument("password", help="password", type=str, default=None)
    parser.add_argument("--admin", help="admin", action="store_true")
    parser.add_argument("--active", help="active", action="store_true")

    args = parser.parse_args()

    if args.action == "add":
        print(add_user(args.email, args.password, args.admin, args.active))


if __name__ == "__main__":
    main()
