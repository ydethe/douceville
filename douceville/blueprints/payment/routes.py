from flask import jsonify, request, render_template
from flask_login import login_required, current_user
import stripe

from douceville import stripe_keys
from douceville.utils import logged, Serializer
from douceville.blueprints.payment import payment_bp


@payment_bp.route("/pay", methods=["GET"])
def pay():
    return render_template('payment/test.html',key=stripe_keys['publishable_key'])

@payment_bp.route('/checkout', methods=['POST'])
def checkout():

    amount = 500

    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='eur',
        description='Flask Charge'
    )

    return render_template('payment/checkout.html', amount=amount)
