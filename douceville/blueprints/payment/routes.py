from flask import jsonify, request, render_template
from flask_login import login_required, current_user
import stripe

from douceville.config import Config
from douceville.utils import logged, Serializer
from douceville.blueprints.payment import payment_bp


@payment_bp.route("/pay", methods=["GET"])
@login_required
def pay():
    return render_template('payment/test.html',user_email=current_user.email,key=Config.STRIPE_PUBLISHABLE_KEY)

@payment_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    return render_template('payment/checkout.html')
