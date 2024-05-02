from flask import Blueprint, render_template
from .models.user import User

bp = Blueprint('profiles', __name__)

# Route to view a user's public profile
@bp.route('/user_profile/<int:user_id>')
def public_profile(user_id):
    # Retrieve user data for the given user_id using a function from the User model
    user = User.public_profile(user_id)
    return render_template('public_profile.html', user=user)
