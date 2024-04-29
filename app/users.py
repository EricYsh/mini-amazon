from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional, InputRequired

from .models.user import User
from .models.orderitem import OrderItem

from flask import Blueprint, jsonify
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])  
    isSeller = BooleanField('Register as seller')
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.register(
            form.email.data,
            form.password.data,
            form.firstname.data,
            form.lastname.data,
            form.address.data,  
            form.isSeller.data  
        )
        if user:
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
        else:
            flash('Registration failed. Email might be already in use or other error occurred.')  
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))



class UserProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    isSeller = BooleanField('Are you a seller?')
    new_password = PasswordField('New Password', validators=[Optional()])
    balance = DecimalField('Balance', validators=[InputRequired()])
    submit = SubmitField('Update Profile')

    def validate_email(self, email):
        if User.email_exists(email.data, exclude_user_id=current_user.id):
            raise ValidationError('This email is already in use by another account.')




@bp.route('/profile', methods=['GET'])
def user_profile():
    user_info = User.show_user_profile(current_user.id)  
    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value')

    if filter_type and filter_value:
        purchases = OrderItem.get_filtered_purchases(current_user.id, filter_type, filter_value)
    else:
        purchases = OrderItem.get_user_purchases(current_user.id)
    
    return render_template('user_profile.html', user=user_info, purchases=purchases)

@bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    user = User.get(current_user.id)
    form = UserProfileForm(obj=user)
    
    if form.validate_on_submit():
        user_updates = {
            'email': form.email.data,
            'firstname': form.firstname.data,
            'lastname': form.lastname.data,
            'address': form.address.data,
            'isSeller': form.isSeller.data,
            'balance': form.balance.data  
        }
        
        if form.new_password.data:
            user_updates['password'] = User.set_password(form.new_password.data)

        success = User.update_user_profile(current_user.id, **user_updates)
        if success:
            flash('Your profile has been updated.')
            return redirect(url_for('users.user_profile')) 
        else:
            flash('Failed to update profile.')

    return render_template('edit_profile.html', form=form)

@bp.route('/get-filter-options', methods=['GET'])
def get_filter_options():
    filter_type = request.args.get('type')
    user_id = current_user.id  
    options = OrderItem.get_filter_options(filter_type, user_id)
    return jsonify(options)

@bp.route('/get-filtered-purchases')
def get_filtered_purchases():
    user_id = current_user.id  
    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value')
    
    purchases = OrderItem.get_filtered_purchases(user_id, filter_type, filter_value)
    
    return jsonify(purchases)

@bp.route('/get-purchases-by-category', methods=['GET'])
def get_purchases_by_category():
    user_id = current_user.id
    category_data = OrderItem.get_purchases_by_category(user_id)
    return jsonify(category_data)