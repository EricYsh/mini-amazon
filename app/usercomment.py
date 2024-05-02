from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models.productcomment import ProductComment
from .models.sellercomment import SellerComment
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

# Create a Blueprint for user comments
bp = Blueprint('usercomment', __name__)

# Form for editing product comments
class EditProductCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rate = IntegerField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Comment')

# Form for editing seller comments
class EditSellerCommentForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired()])
    rate = IntegerField('Rate', validators=[DataRequired()])
    submit = SubmitField('Update Comment')

# Route to display user comments
@bp.route('/usercomments', methods=['GET'])
@login_required
def usercomments():
    # Fetch comments made by the current user
    product_comments = ProductComment.get_product_comments_by_user(current_user.id)
    seller_comments = SellerComment.get_seller_comments_by_user(current_user.id)
    return render_template('usercomment.html', product_comments=product_comments, seller_comments=seller_comments)

# Route to edit a specific product comment
@bp.route('/edit_product_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_product_comment(comment_id):
    # Retrieve the comment by ID
    comment = ProductComment.get_comment_by_id(comment_id)
    if not comment:
        flash('No comment found with the given ID.', 'error')
        return redirect(url_for('usercomment.usercomments'))

    if comment.userid != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('usercomment.usercomments'))

    form = EditProductCommentForm(obj=comment)
    if form.validate_on_submit():
        # Update comment and redirect if form submission is successful
        comment.comment = form.comment.data
        comment.rate = form.rate.data
        comment.update()
        flash('Comment updated successfully.', 'success')
        return redirect(url_for('usercomment.usercomments'))

    return render_template('edit_comment.html', form=form, comment_id=comment_id)

# Route to delete a specific product comment
@bp.route('/delete_product_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_product_comment(comment_id):
    # Delete comment and handle non-existence or unauthorized access
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

# Route to edit a specific seller comment
@bp.route('/edit_seller_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def edit_seller_comment(comment_id):
    # Fetch and update seller comment similarly as product comments
    comment = SellerComment.get_comment_by_id(comment_id)
    if not comment:
        flash('No comment found.', 'error')
        return redirect(url_for('usercomment.usercomments'))

    form = EditSellerCommentForm(obj=comment)
    if form.validate_on_submit():
        comment.comment = form.comment.data
        comment.rate = form.rate.data
        comment.update()
        flash('Comment updated successfully.', 'success')
        return redirect(url_for('usercomment.usercomments'))

    return render_template('edit_seller_comment.html', form=form, comment=comment)

# Route to delete a specific seller comment
@bp.route('/delete_seller_comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_seller_comment(comment_id):
    # Directly delete seller comment without fetching it
    SellerComment.delete_comment(comment_id)
    flash('Comment deleted successfully.', 'success')
    return redirect(url_for('usercomment.usercomments'))
