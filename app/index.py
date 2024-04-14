from flask import render_template
from flask_login import current_user
import datetime
from flask import request, redirect, url_for

from .models.product import Product
from .models.order import Order

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return redirect(url_for('product.product'))
    # # get all available products for sale:
    # products = Product.get_all()
    # # find the products current user has bought:
    # if current_user.is_authenticated:
    #     orders = Order.get_all_by_uid_since(
    #         current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    # else:
    #     orders = None
    # # render the page by adding information to the index.html file
    # return render_template('index.html',
    #                        avail_products=products,
    #                        purchase_history=orders)
