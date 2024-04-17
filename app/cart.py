# This class is no longer used in the following milestones.

from flask import render_template
from flask_login import current_user
from flask import redirect, url_for, request, flash

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
        total_quantity = 0
        total_price = 0
        for item in cart_items:
            total_quantity += item['quantity']
            total_price += item['price'] * item['quantity']

    else:
        cart_items = None
    return render_template('cart.html',
                       items=cart_items,
                       items_saved=cart_items_saved,
                       total_quantity=total_quantity,
                       total_price=total_price)


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
def cart_add(product_id):
    # add a product to the current user's cart
    if current_user.is_authenticated:
        # Retrieve quantity from the form data
        quantity = request.form.get('quantity', type=int, default=1)
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

@bp.route('/cart', methods=['POST'])
def cart_and_save():
    # move a product from the cart to the saved for later list
    cart_id = request.form.get('cart_id')
    in_cart = request.form.get('in_cart')
    seller_inventory_id = request.form.get('sellerinventoryid')
    print("Received form data:", request.form)
    if cart_id is None:
        flash('Invalid request.', 'error')
    
    success = Cart.move_to_from_saved_for_later(cart_id, in_cart, seller_inventory_id)
    if success:
        flash('Item moved.', 'success')
    else:
        flash('Item could not be moved.', 'error')

    return redirect(url_for('cart.cart'))


@bp.route('/cart', methods=['POST'])
def remove():
    """
    Remove a product from the user's cart.
    """
    cart_id = request.form.get('cart_id')  # Get cart_id from form data
    try:
        if cart_id is None:
            flash('Invalid request.', 'error')
            return redirect(url_for('cart.cart'))

        # Assuming `Cart` has a method `remove_item` that removes an item by user ID and cart ID
        success = Cart.remove_item(current_user.id, cart_id)
        if success:
            flash('Item removed from cart successfully.', 'success')
        else:
            flash('Item could not be removed.', 'error')
    except Exception as e:
        # Log the error and show an error message
        print(f"Error removing item: {e}")
        flash('Error removing item from cart.', 'error')

    return redirect(url_for('cart.cart'))

@bp.route('/cart', methods=['POST'])
def checkout():

    return None