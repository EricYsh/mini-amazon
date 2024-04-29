from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from .models.product import Product
from .models.productcomment import ProductComment

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/product', methods=['GET'])
def product():
    page = request.args.get('page', 1, type=int)
    total_products = Product.get_product_number()
    per_page = 20
    total_pages = (total_products + per_page - 1) // per_page
    print("total_products", total_products, "total_pages", total_pages)
    product_items = Product.get_expensive_products_paged(page, per_page)
    categories = Product.get_all_categories()
    return render_template('products.html', products=product_items, categories=categories, current_page=page, total_pages=total_pages)


@bp.route('/product/search', methods=['GET'])
def product_search():
    search = request.args.get('keyword', '')
    search_type = request.args.get('search_type', 'name')
    category_id = request.args.get('category', None)
    sort = request.args.get('sort', None)
    page = request.args.get('page', 1, type=int)
    min_rating = request.args.get('min_rating', None, type=int)
    min_price = request.args.get('min_price', None, type=float)  
    max_price = request.args.get('max_price', None, type=float) 
    per_page = 20
    print(search, search_type, category_id, sort, page, min_rating, min_price, max_price)

    if search_type == 'name':
        all_products = Product.search_products_by_name(search, category_id, min_rating, min_price, max_price)
    elif search_type == 'description':
        all_products = Product.search_products_by_description(search, category_id, min_rating, min_price, max_price)
    else:
        return render_template('404.html')

    if sort:
        reverse = True if 'desc' in sort else False
        key = 'price' if 'price' in sort else 'rating'
        all_products = sorted(all_products, key=lambda x: getattr(x, key), reverse=reverse)

    total_products = len(all_products)
    total_pages = (total_products + per_page - 1) // per_page
    print("total_products", total_products, "total_pages", total_pages)
    start = (page - 1) * per_page
    end = start + per_page
    products = all_products[start:end]

    categories = Product.get_all_categories()
    return render_template('products.html', products=products, categories=categories, search_type=search_type, sort=sort, selected_category=category_id, current_page=page, total_pages=total_pages)



@bp.route('/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.get_product_by_id(product_id)
    sellers = Product.get_sellers(product_id)
    reviews = Product.get_reviews(product_id)
    print("product", product.description)
    return render_template('product_detail.html', product=product, sellers = sellers, reviews = reviews, product_id=product_id) 


@bp.route('/product_add', methods=['GET'])
def product_add():
    categories = Product.get_all_categories()
    return render_template('product_add.html', categories=categories)



@bp.route('/product_edit', methods=['POST'])
def product_edit():
    categories = Product.get_all_categories()
    item_details = {
    'name': request.form['item_name'],
    'image': request.form['item_image'],
    'price': request.form['item_price'],
    'quantity': request.form['item_quantity'],
    'id': request.form['item_id']
    }
    print(item_details)
    return render_template('product_edit.html', categories=categories, item_details=item_details)

@bp.route('/product_remove', methods=['POST'])
def product_remove():
    item_details = {
    'name': request.form['item_name'],
    'image': request.form['item_image'],
    'price': request.form['item_price'],
    'quantity': request.form['item_quantity'],
    'id': request.form['item_id']
    }
    print(item_details)

    return render_template('product_edit.html', item_details=item_details)



@bp.route('/add_comment', methods=['POST'])
def add_comment():
   
    comment = request.form['comment']
    product_id = request.form['product_id']
    rating = request.form['rating']
    
    
    ProductComment.insert_comment(comment, product_id, rating, current_user.id)

    

    return redirect(url_for('product.product_detail', product_id=product_id))