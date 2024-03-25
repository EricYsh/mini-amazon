# app/purchases.py
from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from .models.orderitem import OrderItem  

bp = Blueprint('purchases', __name__)

@bp.route('/user_purchases')
@login_required
def user_purchases():
    purchases = OrderItem.get_user_purchases(current_user.id)
    return render_template('user_purchases.html', purchases=purchases)
