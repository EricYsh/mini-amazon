# This file perfroms Social Guru
# Given a user id, find the 5 most recent feedback they posted
from flask import Blueprint, jsonify, request
from .models.productcomment import ProductComment
from .models.sellercomment import SellerComment
from flask_login import current_user
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

bp = Blueprint('usercomment', __name__)

class EditCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rate = IntegerField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Comment')

@bp.route('/usercomments', methods=['GET'])
def usercomments():
    # Use ProductComment get_comments_by_user(userid)
    product_comments = ProductComment.get_product_comments_by_user(current_user.id)
    seller_comments = SellerComment.get_seller_comments_by_user(current_user.id)
    # return the comments in JSON format
    return render_template('usercomment.html',
                       product_comments=product_comments,
                       seller_comments=seller_comments)

# test
@bp.route('/edit_product_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_product_comment(comment_id):
    comment = ProductComment.query.get_or_404(comment_id)
    if comment.userid != current_user.id:
        abort(403)  # Ensure that the current user owns the comment
    form = EditCommentForm(obj=comment)
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.rate = form.rate.data
        db.session.commit()
        flash('Your comment has been updated.')
        return redirect(url_for('usercomment.usercomments'))
    return render_template('edit_comment.html', form=form, title='Edit Product Comment')

@bp.route('/edit_seller_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_seller_comment(comment_id):
    comment = SellerComment.query.get_or_404(comment_id)
    if comment.userid != current_user.id:
        abort(403)  # Ensure that the current user owns the comment
    form = EditCommentForm(obj=comment)
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.rate = form.rate.data
        db.session.commit()
        flash('Your comment has been updated.')
        return redirect(url_for('usercomment.usercomments'))
    return render_template('edit_comment.html', form=form, title='Edit Seller Comment')
