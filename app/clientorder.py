from flask import render_template, redirect, url_for, request
from flask_login import current_user
from .models.orderitem import OrderItem

from flask import Blueprint
bp = Blueprint('clientorder', __name__)


@bp.route('/clientorder', methods=['GET'])
def clientorder():
    
    return render_template('products.html', products=product_items, categories=categories, current_page=page, total_pages=total_pages)
