from flask import render_template, redirect, url_for, request
from flask_login import current_user
from .models.orderitem import OrderItem
from .models.user import User
from .models.order import Order

from flask import Blueprint
bp = Blueprint('clientorder', __name__)


@bp.route('/clientorder', methods=['GET'])
def clientorder():
    client_items = OrderItem.get_client_item(current_user.id)
    return render_template('client_order.html', client_items=client_items)


@bp.route('/clientorderdetial', methods=['POST'])
def clientorderdetail():
    item_info ={
    'product_name' : request.form['product_name'],
    'brought_price' : request.form['brought_price'],
    'quantity' : request.form['quantity'],
    'order_time' : request.form['order_time'],
    'order_status' : request.form['order_status'],
    'item_id' : request.form['id']
    }
    # query address, date, user name, email
    buyer_id = OrderItem.get_buyerid_by_itemid(item_info['item_id'])
    user_info = User.show_user_profile(buyer_id)



    return render_template('order_detail.html', user_info=user_info, item_info=item_info)
    # return render_template('order_detail.html')


@bp.route('/fulfillorder', methods=['POST'])
def fulfillorder():
    item_id = request.form['item_id']
    

    # # update current orderitem
    OrderItem.fulfill_orderitem(item_id)

    # # check the fulfillment of the entire order
    order_id = OrderItem.get_order_id(item_id)
    in_process_num = OrderItem.get_in_process_num(order_id)

    if in_process_num == 0:
        Order.set_fulfillment(order_id)


    return redirect(url_for('clientorder.clientorder'))
    # return render_template('order_detail.html')