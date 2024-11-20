import time
from urllib3.util import parse_url

import stripe
from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from flask_login import login_user, logout_user, login_required, current_user

from . import users_bp
from .forms import LoginForm, SignupForm


@users_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    from ...config import config

    return_url = "%s:%s%s" % (config.HOST, config.PORT, url_for(".profile"))
    sid = current_user.getStripeID()

    session = stripe.billing_portal.Session.create(customer=sid, return_url=return_url)

    t = current_user.getCurrentPeriodEnd()
    if current_user.admin:
        dt = "Permanent (admin)"
    elif t < 0:
        dt = "Inactif"
    else:
        ts = time.gmtime(t)
        dt = "Jusqu'au " + time.strftime("%A %d %B à %Hh%M", ts)

    return render_template(
        "profile.html",
        user_email=current_user.email,
        subscription_end=dt,
        portal_url=session.url,
        publishableKey=config.STRIPE_PUBLISHABLE_KEY,
        price_id=config.PRICE_ID,
    )


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    from ...models import User

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.isCorrectPassword(form.password.data):
            flash("Please check your login details and try again.")
            return redirect(
                url_for(".login")
            )  # if the user doesn't exist or password is wrong, reload the page
        elif not user.active:
            flash("Your account has not been confirmed yet.")
            return redirect(url_for(".login"))
        else:
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or parse_url(next_page).netloc != "":
                next_page = url_for("carte.recherche")
            return redirect(next_page)

    return render_template("login.html", form=form)


@users_bp.route("/signup", methods=["GET", "POST"])
def signup():
    from ...blueprints.users.manage_users import add_user

    form = SignupForm()

    if form.validate_on_submit():
        lstat = add_user(email=form.email.data, pwd=form.password.data, admin=False, active=False)
        if lstat:
            return redirect(url_for("carte.carte"))
        else:
            flash("Email address already exists")
            return redirect(url_for(".signup"))

    return render_template("signup.html", form=form)


@users_bp.route("/confirm", methods=["GET"])
def confirm():
    from ...utils import Serializer
    from ...models import db, User
    from .. import logger

    token = request.args.get("token", "")

    s = Serializer()
    param = s.deserialize(token, ttl=86400)

    verif_email = param["email"]
    maj_user = {"active": True}
    maj_user.update(param)

    q = db.session.query(User).filter(User.email == verif_email)
    if q.count() == 0:
        logger.error("Aucun utilisateur avec le mail %s" % verif_email)
    else:
        q.update(maj_user)
        db.session.commit()

    return redirect(url_for(".login"))


@users_bp.route("/logout", methods=["GET"])
def logout():

    logout_user()

    return redirect(url_for(".login"))
