from flask import render_template
from flask_login import current_user
from flask import jsonify
import datetime


from .models.product import Product
from .models.purchase import Purchase
from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('/wishlist', __name__)


@bp.route('/wishlist')
def wishlist():
    # get all wishlist items from the database for current user and display them
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        items = WishlistItem.get_all_by_uid(current_user.id)
    else:
        return jsonfiy({}), 404
    return jsonify([item.__dict__ for item in items])
