from flask import render_template, redirect, url_for, request
from flask_login import current_user
from .models.orderitem import OrderItem

from flask import Blueprint
bp = Blueprint('clientorder', __name__)


@bp.route('/clientorder', methods=['GET'])
def clientorder():
    client_items = OrderItem.get_client_item(current_user.id)
    return render_template('client_order.html', client_items=client_items)


@bp.route('/clientorderdetial', methods=['POST'])
def clientorderdetail():
    product_name = request.form['product_name']
    brought = request.form['productImage']
    price = request.form['productPrice']
    description = request.form['productDescription']
    quantity = request.form['productQuantity']
    category = request.form['category']