# This class is no longer used in the following milestones.

from flask import render_template
from flask_login import current_user
from flask import jsonify
from flask import redirect, url_for
import datetime
from humanize import naturaltime


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
        items = None
        # return jsonfiy({}), 404
    # return jsonify([item.__dict__ for item in items])
    return render_template('wishlist.html',
                       items=items,
                       humanize_time=humanize_time)


@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    # add a product to the current user's wishlist
    if current_user.is_authenticated:
        WishlistItem.add_wishlist_item(current_user.id, product_id, datetime.datetime.now())
    else:
        # TODO redirect it to an error page
        return None
    return redirect(url_for('/wishlist.wishlist'))


def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)
