from flask import render_template, redirect, url_for, request

from .models.product import Product

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
    per_page = 20  
    print(search, search_type, category_id, sort, page)
 
    if search_type == 'name':
        all_products = Product.search_products_by_name(search, category_id)
    elif search_type == 'description':
        all_products = Product.search_products_by_description(search, category_id)
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
    return render_template('product_detail.html', product=product, sellers = sellers, reviews = reviews) 


@bp.route('/product_add', methods=['GET'])
def add_product():
    categories = Product.get_all_categories()
    return render_template('product_add.html', categories=categories)

