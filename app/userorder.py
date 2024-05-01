from flask import render_template, redirect, url_for, request, flash, session
from flask_login import current_user
from .models.orderitem import OrderItem
from .models.user import User
from .models.order import Order
from .models.cart import Cart
from .models.sellerinventory import SellerInventory

from flask import Blueprint

bp = Blueprint('userorder', __name__)


@bp.route('/userorder', methods=['GET'])
def userorder():
    orders = Order.get_order_by_user_id(current_user.id)    
    return render_template('user_order_detail.html', orders=orders)

@bp.route('/userorder/<int:order_id>', methods=['GET'])
def view_order(order_id):
    order_items = OrderItem.get_order_items_by_order_id(order_id)
    order = Order.get_order_by_id(order_id)
    return render_template('user_orderitem_detail.html', order_items=order_items, order=order)

@bp.route('/checkout', methods=['POST'])
def checkout():
    if not current_user.is_authenticated:
        flash("Please log in to proceed with checkout.", "warning")
        return redirect(url_for('users.login'))

    # Retrieve the user's cart items that are not saved for later
    cart_items = Cart.get_all_by_uid(current_user.id)

    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.cart'))
    
    # cart_items = [{'name': row[0], 'image': row[1], 'price': row[2], 'quantity': row[3], 
    #                    'productid': row[4], 'cartid': row[5], 'sellerinventoryid': row[6], 'sellerid': row[7]} for row in rows]

    # Check user balance and inventory availability
    total_cost = 0
    for item in cart_items:
        total_cost += item['quantity'] * item['price']
    print(f"Total cost: {total_cost}")

    user_balance = User.get_user_balance(current_user.id)
    print(f"User balance: {user_balance}")
    if user_balance < total_cost:
        flash("Insufficient balance to complete the purchase.", "danger")
        return redirect(url_for('cart.cart'))

    for item in cart_items:
        inventory_quantity = SellerInventory.get_quantity_by_id(item['sellerinventoryid'])
        if inventory_quantity < item['quantity']:
            flash(f"Insufficient inventory for {item['name']}.", "danger")
            return redirect(url_for('cart.cart'))

    # All checks passed, proceed with order creation
    new_order_id = Order.create_order(current_user.id)

    # orderid, productid, sellerid, quantity, brought_price
    for item in cart_items:
        order_item = OrderItem.create_order_item(
            orderid=new_order_id,
            productid=item['productid'],
            sellerid=item['sellerid'],
            quantity=item['quantity'],
            brought_price=item['price'],  # Assuming price is available here; adjust as needed
        )

        # Update inventory quantity
        inventory_quantity_old = SellerInventory.get_quantity_by_id(item['sellerinventoryid'])
        SellerInventory.update_inventory_quantity(item['sellerinventoryid'], inventory_quantity_old - item['quantity'])

        # Remove item from cart
        Cart.remove_item(current_user.id, item['cartid'])

    # Deduct total cost from user's balance
    User.update_user_balance(current_user.id, total_cost)

    flash("Checkout successful!", "success")
    return redirect(url_for('userorder.userorder'))
