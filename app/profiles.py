# app/profiles.py
from flask import Blueprint, render_template
from .models.user import User

bp = Blueprint('profiles', __name__)

@bp.route('/user_profile/<int:user_id>')
def public_profile(user_id):
    user = User.public_profile(user_id)
    return render_template('public_profile.html', user=user)
