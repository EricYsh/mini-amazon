from flask import render_template, redirect, url_for, request

from .models.product import Product

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        # k = request.form.get('k')
        # if k.isdigit():  # Ensure k is a number
        #     k = int(k)  # Convert k to an integer
        product_items = Product.get_top_k_expensive_products(20)  # Use k as the parameter
        categories = Product.get_all_categories()  
        return render_template('products.html', products=product_items, categories=categories)  # Pass the product_items variable
    return render_template('404.html')

@bp.route('/product/search', methods=['GET'])
def product_search():
    search = request.args.get('keyword', '')
    search_type = request.args.get('search_type', 'name')
    category_id = request.args.get('category', None)  # 获取类别ID
    sort = request.args.get('sort', None)

    # 根据搜索类型和类别筛选产品
    if search_type == 'name':
        products = Product.search_products_by_name(search, category_id)
    elif search_type == 'description':
        products = Product.search_products_by_description(search, category_id)
    else:
        return render_template('404.html')

    # 排序逻辑保持不变
    if sort:
        reverse = True if 'desc' in sort else False
        key = 'price' if 'price' in sort else 'rating'
        products = sorted(products, key=lambda x: getattr(x, key), reverse=reverse)

    categories = Product.get_all_categories()  
    return render_template('products.html', products=products, categories=categories, search_type=search_type, sort=sort, selected_category=category_id)



@bp.route('/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.get_product_by_id(product_id)
    sellers = Product.get_sellers(product_id)
    reviews = Product.get_reviews(product_id)
    return render_template('product_detail.html', product=product, sellers = sellers, reviews = reviews) 


@bp.route('/product_add', methods=['GET'])
def add_product():
    categories = Product.get_all_categories()
    return render_template('product_add.html', categories=categories)

