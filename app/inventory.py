# This class is no longer used in the following milestones.

from flask import render_template
from flask_login import current_user
from flask import redirect, url_for


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
