from flask import (
    render_template,
    request,
    redirect,
    url_for,
)
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse

from douceville.blueprints.users.manage_users import add_user
from douceville.config import Config
from douceville.utils import logged, Serializer
from douceville.blueprints.users import users_bp
from douceville.blueprints.users.forms import LoginForm, SignupForm
from douceville.models import db, User


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.isCorrectPassword(form.password.data):
            flash('Please check your login details and try again.')
            return redirect(url_for('.login')) # if the user doesn't exist or password is wrong, reload the page
        elif not user.is_active:
            flash('Your account has not been confirmed yet.')
            return redirect(url_for('.login'))
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)

    return render_template("users/login.html", form=form)


@users_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        lstat = add_user(email=form.email.data, pwd=form.password.data, admin=False)
        if lstat:
            return redirect(url_for("index"))
        else:
            flash('Email address already exists')
            return redirect(url_for(".signup"))

    return render_template("users/signup.html", form=form)

@users_bp.route("/confirm", methods=["GET"])
def confirm():
    token = request.args.get("token", "")
    
    s = Serializer()
    param = s.deserialize(token, ttl=86400)

    verif_email = param['email']
    maj_user = {'is_active':True}
    maj_user.update(param)

    q = db.session.query(User).filter(User.email == verif_email)
    if q.count() == 0:
        logging.error("Aucun utilisateur avec le mail %s" % verif_email)
    else:
        q.update(maj_user)
    
    db.session.commit()

    return redirect(url_for(".login"))

@users_bp.route("/logout", methods=["GET"])
def logout():
    logout_user()

    return redirect(url_for("index"))
