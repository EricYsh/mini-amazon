from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models.productcomment import ProductComment
from .models.sellercomment import SellerComment
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

bp = Blueprint('usercomment', __name__)

class EditProductCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rate = IntegerField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Comment')

class EditSellerCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rate = IntegerField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Comment')

@bp.route('/usercomments', methods=['GET'])
@login_required
def usercomments():
    product_comments = ProductComment.get_product_comments_by_user(current_user.id)
    seller_comments = SellerComment.get_seller_comments_by_user(current_user.id)
    print(product_comments)
    return render_template('usercomment.html', product_comments=product_comments, seller_comments=seller_comments)

@bp.route('/edit_product_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_product_comment(comment_id):
    comment = ProductComment.get_comment_by_id(comment_id)
    if not comment:
        flash('No comment found with the given ID.', 'error')
        return redirect(url_for('usercomments'))

    if comment.userid != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('usercomments'))

    form = EditProductCommentForm(obj=comment)
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.rate = form.rate.data
        comment.update()
        flash('Comment updated successfully.', 'success')
        return redirect(url_for('usercomment.usercomments'))

    return render_template('edit_comment.html', form=form, comment_id=comment_id)


@bp.route('/edit_seller_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_seller_comment(comment_id):
    comment = SellerComment.get_comment_by_id(comment_id)
    if comment.user_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('usercomment.usercomments'))

    form = EditSellerCommentForm(obj=comment)
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.rate = form.rate.data
        comment.save()
        flash('Comment updated successfully.', 'success')
        return redirect(url_for('usercomment.usercomments'))

    return render_template('edit_comment.html', form=form, comment_id=comment_id)

@bp.route('/delete_product_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_product_comment(comment_id):
    comment = ProductComment.get_comment_by_id(comment_id)
    if not comment:
        flash('No comment found with the given ID.', 'error')
        return redirect(url_for('usercomment.usercomments'))
    
    if comment.userid != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('usercomment.usercomments'))

    ProductComment.delete_comment(comment_id)
    flash('Comment deleted successfully.', 'success')
    return redirect(url_for('usercomment.usercomments'))
