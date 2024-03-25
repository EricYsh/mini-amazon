# This class is no longer used in the following milestones.

from flask import render_template, redirect, url_for, request

from .models.product import Product

from flask import Blueprint
bp = Blueprint('product', __name__)


@bp.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        k = request.form.get('k')
        if k.isdigit():  # 确保k是数字
            k = int(k)  # 将k转换为整数
            product_items = Product.get_top_k_expensive_products(k)  # 使用k作为参数
            return render_template('products.html', products=product_items)  # 传递product_items变量        return render_template('products.html', products=products)
    return render_template('find_products.html')