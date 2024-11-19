import json

import stripe
from flask import request, jsonify, url_for
from flask_login import login_required, current_user

from ...config import config
from ...blueprints.payment import payment_bp


@payment_bp.route("/create-checkout-session", methods=["POST"])
@login_required
def create_checkout_session():
    data = json.loads(request.data)
    domain_url = "%s:%s" % (config.HOST, config.PORT)

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url="%s%s" % (domain_url, url_for("users.profile")),
            cancel_url="%s%s" % (domain_url, url_for("users.profile")),
            payment_method_types=["card"],
            mode="subscription",
            customer=current_user.getStripeID(),
            line_items=[{"price": data["priceId"], "quantity": 1}],
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify({"error": {"message": str(e)}}), 400
