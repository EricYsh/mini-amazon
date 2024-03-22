# This class is no longer used in the following milestones.

from flask import render_template
from flask_login import current_user
from flask import redirect, url_for


from .models.product import Product
from .models.cart import Cart

from flask import Blueprint
bp = Blueprint('cart', __name__)


@bp.route('/cart')
def cart():
    # get all cart items from the database for current user and display them
    
    # find the products current user has in cart:
    if current_user.is_authenticated:
        cart_items = Cart.get_all_by_uid(current_user.id)
        cart_items_saved = Cart.get_all_by_uid(current_user.id, saved_for_later=True)
    else:
        cart_items = None
    return render_template('cart.html',
                       items=cart_items,
                       items_saved=cart_items_saved)
