from flask import render_template, redirect, url_for, request
from flask_login import current_user
from .models.product import Product

from flask import Blueprint
bp = Blueprint('trend', __name__)


@bp.route('/trend', methods=['GET'])
def trend():
    # get top 5 products
    """
    Displays the top 5 trending products.
    This route handles the 'GET' method to fetch and display the top five products based on some criteria defined in the Product model.
    Returns:
        Rendered template: The 'trend.html' page populated with the top five products.
    """
    products = Product.get_topfive_products()
    return render_template('trend.html', products=products)

