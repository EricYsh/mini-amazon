from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from .models.product import Product
from .models.productcomment import ProductComment

from flask import Blueprint
bp = Blueprint('product', __name__)

# Route for displaying the product page with pagination of expensive products.
@bp.route('/product', methods=['GET'])
def product():
    page = request.args.get('page', 1, type=int)
    total_products = Product.get_product_number()  # Get total number of products.
    per_page = 20  # Products per page.
    total_pages = (total_products + per_page - 1) // per_page  # Calculate total pages.
    product_items = Product.get_expensive_products_paged(page, per_page)  # Fetch products for the current page.
    categories = Product.get_all_categories()  # Fetch all product categories.
    return render_template('products.html', products=product_items, categories=categories, current_page=page, total_pages=total_pages)

# Route for searching products based on name or description.
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
    if search_type == 'name':
        all_products = Product.search_products_by_name(search, category_id, min_rating, min_price, max_price)
    elif search_type == 'description':
        all_products = Product.search_products_by_description(search, category_id, min_rating, min_price, max_price)
    else:
        return render_template('404.html')  # Render 404 page if search type is invalid.
    if sort:  # Optional sorting of results.
        reverse = True if 'desc' in sort else False
        key = 'price' if 'price' in sort else 'rating'
        all_products = sorted(all_products, key=lambda x: getattr(x, key), reverse=reverse)
    total_products = len(all_products)
    total_pages = (total_products + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    products = all_products[start:end]
    categories = Product.get_all_categories()
    return render_template('products.html', products=products, categories=categories, search_type=search_type, sort=sort, selected_category=category_id, current_page=page, total_pages=total_pages)

# Route for displaying detailed information about a specific product.
@bp.route('/products/<int:product_id>', methods=['GET'])
def product_detail(product_id):
    product = Product.get_product_by_id(product_id)  # Fetch the product by ID.
    sellers = Product.get_sellers(product_id)  # Fetch sellers of this product.
    reviews = Product.get_reviews(product_id)  # Fetch reviews for this product.
    return render_template('product_detail.html', product=product, sellers=sellers, reviews=reviews, product_id=product_id)

# Route for initiating adding a product (shows a form to add).
@bp.route('/product_add', methods=['GET'])
def product_add():
    categories = Product.get_all_categories()  # Fetch all categories for the form.
    return render_template('product_add.html', categories=categories)

# Route for handling the editing of a product (after form submission).
@bp.route('/product_edit', methods=['POST'])
def product_edit():
    categories = Product.get_all_categories()  # Fetch all categories for dropdown in edit form.
    item_details = {
        'name': request.form['item_name'],
        'image': request.form['item_image'],
        'price': request.form['item_price'],
        'quantity': request.form['item_quantity'],
        'id': request.form['item_id']
    }
    return render_template('product_edit.html', categories=categories, item_details=item_details)

# Route for handling the removal of a product (might be part of the edit form).
@bp.route('/product_remove', methods=['POST'])
def product_remove():
    item_details = {
        'name': request.form['item_name'],
        'image': request.form['item_image'],
        'price': request.form['item_price'],
        'quantity': request.form['item_quantity'],
        'id': request.form['item_id']
    }
    return render_template('product_edit.html', item_details=item_details)

# Route for adding a product comment by a logged-in user.
@bp.route('/add_comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    product_id = request.form['product_id']
    rating = request.form['rating']
    ProductComment.insert_comment(comment, product_id, rating, current_user.id)  # Save the new comment to the database.
    return redirect(url_for('product.product_detail', product_id=product_id))  # Redirect back to the product detail page.
