# This file perfroms Social Guru
# Given a user id, find the 5 most recent feedback they posted
from flask import Blueprint, jsonify, request
from .models.productcomment import ProductComment

bp = Blueprint('usercomment', __name__, url_prefix='/usercomments')

@bp.route('/<int:userid>', methods=['GET'])
def get_user_comments(userid):
    # Use ProductComment get_comments_by_user(userid)
    comments = ProductComment.get_comments_by_user(userid)
    # return the comments in JSON format
    return jsonify(comments)

