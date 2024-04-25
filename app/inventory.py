# This class is no longer used in the following milestones.

from flask import render_template
from flask_login import current_user
from flask import redirect, url_for, request


from .models.product import Product
from .models.sellerinventory import SellerInventory

from flask import Blueprint
bp = Blueprint('inventory', __name__)


@bp.route('/inventory')
def inventory():
    # get all cart items from the database for current user and display them
    
    # find the products current user has in cart:
    if current_user.is_authenticated and current_user.isSeller:
        inventory_items = SellerInventory.get_all_by_uid(current_user.id)
    else:
        cart_items = None
    return render_template('inventory.html',
                       items=inventory_items)


@bp.route('/add_product', methods=['POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['productName']
        image = request.form['productImage']
        price = request.form['productPrice']
        description = request.form['productDescription']
        quantity = request.form['productQuantity']
        category = request.form['category']

        print(name, image, price, quantity,description, current_user.id, category)
        
        reply = SellerInventory.insert_new_product(current_user.id, name, description, image, price, quantity, category)
        if reply == 'success':
            return redirect(url_for('inventory.inventory'))
        else:
            return redirect(url_for('inventory.add_product'))
    
@bp.route('/edit_product/<item_id>', methods=['POST'])
def edit_product():
    if request.method == 'POST':
        product_id = request.form['productID']
        name = request.form['productName']
        image = request.form['productImage']
        price = request.form['productPrice']
        quantity = request.form['productQuantity']
        print(product_id, name, image, price, quantity)
        return redirect(url_for('inventory.inventory'))


