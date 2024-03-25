# This file perfroms Social Guru
# Given a user id, find the 5 most recent feedback they posted
from flask import Blueprint, jsonify, request
from .models.productcomment import ProductComment
from .models.sellercomment import SellerComment
from flask_login import current_user
from flask import render_template

bp = Blueprint('usercomment', __name__)

@bp.route('/usercomments', methods=['GET'])
def usercomments():
    # Use ProductComment get_comments_by_user(userid)
    product_comments = ProductComment.get_product_comments_by_user(current_user.id)
    seller_comments = SellerComment.get_seller_comments_by_user(current_user.id)
    # return the comments in JSON format
    return render_template('usercomment.html',
                       product_comments=product_comments,
                       seller_comments=seller_comments)

