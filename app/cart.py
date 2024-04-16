# This class is no longer used in the following milestones.

from flask import render_template
from flask_login import current_user
from flask import redirect, url_for
from flask import request

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


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    # add a product to the current user's cart
    if current_user.is_authenticated:
        # Retrieve quantity from the form data
        quantity = request.form.get('quantity', type=int, default=1)
        print("front end quantity:", quantity)
        success = Cart.add_cart_item(current_user.id, quantity, False, product_id)
        print("Add successfully", success)
    else:
        # TODO redirect it to an error page
        return None
    return redirect(url_for('cart.cart'))



@bp.route('/cart/add_saved_for_later/<int:product_id>', methods=['POST'])
def cart_add_saved_for_later(product_id):
    # add a product to the current user's cart's saved for later list
    if current_user.is_authenticated:
        print("Received form data:", request.form)
        quantity = request.form.get('quantity', type=int, default=1)
        success = Cart.add_cart_item(current_user.id, quantity, True, product_id)
        print("Save for later successfully", success)
    else:
        # TODO redirect it to an error page
        return None
    return redirect(url_for('cart.cart'))
