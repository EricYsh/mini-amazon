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
    """
    Handles the addition of a new product to the inventory through a POST request.
    Collects product details from the form and adds them to the database.
    Redirects:
        Success: Redirects to the inventory page.
        Failure: Redirects to the add product page to retry the input.
    """
    if request.method == 'POST':
        name = request.form['productName']
        image = request.form['productImage']
        price = request.form['productPrice']
        description = request.form['productDescription']
        quantity = request.form['productQuantity']
        category = request.form['category']

        print(name, image, price, quantity,description, current_user.id, category)
        
        reply = SellerInventory.insert_new_product(current_user.id, name, description, image, price, quantity, category)
        if reply == '1':
            return redirect(url_for('inventory.inventory'))
        else:
            return redirect(url_for('product.product_add'))
    
@bp.route('/edit_product', methods=['POST'])
def edit_product():
    """
    Edits an existing product in the inventory via a POST request.
    Updates product details like price and quantity in the database based on form input.
    Redirects:
        Always redirects back to the inventory page after the operation.
    """
    product_id = request.form['productid']
    price = request.form['productPrice']
    quantity = request.form['productQuantity']
    print(product_id, price, quantity)
    reply = SellerInventory.edit_product(product_id, price, quantity)

    return redirect(url_for('inventory.inventory'))

@bp.route('/remove_product', methods=['POST'])
def remove_product():
    """
    Removes a product from the inventory or sets its quantity to zero.
    Processes item details from the form and updates the inventory accordingly.
    Redirects:
        Always redirects back to the inventory page after the operation.
    """
    item_details = {
        'name': request.form['item_name'],
        'image': request.form['item_image'],
        'price': request.form['item_price'],
        'quantity': request.form['item_quantity'],
        'id': request.form['item_id']
    }
    print(item_details)
    reply = SellerInventory.edit_product(item_details['id'], item_details['price'], 0)

    return redirect(url_for('inventory.inventory'))


