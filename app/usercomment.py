# This file perfroms Social Guru
# Given a user id, find the 5 most recent feedback they posted
from flask import Blueprint, render_template
from flask_login import login_required
from .models.productcomment import ProductComment
from .db import db

bp = Blueprint('usercomments', __name__)

@bp.route('/usercomments/<int:user_id>')
@login_required
def user_comments(user_id):
    comments = ProductComment.query.filter_by(user_id=user_id).order_by(ProductComment.time_commented.desc()).limit(5).all()
    return render_template('user_comments.html', comments=comments)
