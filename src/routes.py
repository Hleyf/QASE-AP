from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session, current_app
from flask_login import login_required, current_user, login_user
from models import User
from services import UserService


main = Blueprint('main', __name__)
service = UserService()

@main.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('main.login'))        
    else:
        return redirect(url_for('main.home'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = service.login()
        if user:
            login_user(user)
            return redirect(url_for('main.home'))            
        else:
            return render_template('auth/login.html', error="Invalid credentials")
    elif request.method == 'GET' and 'user' not in session:
        return render_template('auth/login.html')
    elif request.method == 'GET' and 'user' in session:
        return redirect(url_for('main.home'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_user = User(
            user_name=request.form['user_name'],
            password=request.form['password'],
            full_name=request.form['full_name'],
            email=request.form['email'],
            role='user',
            created_at=datetime.now(),
            created_by= None
        )
        with current_app.app_context():
            user = service.create_user(form_user)
        
        if user:
            return redirect(url_for('main.login'))
        else:
            return render_template('auth/register.html', error="Invalid credentials")
    elif request.method == 'GET' and 'user_id' not in session:
        return render_template('auth/register.html')

@main.route('/home')
@login_required
def home():
    # get all the users from the database
    users = service.get_all_users()
    is_admin = current_user.role == 'admin'

    return render_template('pages/home.html', users=users, is_admin=is_admin, logged_user_id=current_user.id)
    
#Get method to return user.id by email
@main.route('/user/<email>', methods=['GET'])
def check_email_availability(email):
    response = service.get_email_availability(email)
    return response

@main.route('/users/<id>/edit', methods=['GET','POST'])
def update_user(id):
    if request.method == 'GET':
        is_admin = current_user.role == 'admin'
        user = service.get_user_by_id(id)
        is_user = current_user.id == user.id
        return render_template('pages/edit-modal.html', is_admin=is_admin, is_user = is_user, user=user)
    elif request.method == 'POST':
        user_id = service.update_user(id)
        if user_id:
            return redirect(url_for('main.home'))
        else:
            return render_template('pages/edit-modal.html', error="Invalid credentials")
        
@main.route('/users/<id>/delete', methods=['DELETE'])
def delete_user(id):
    UserService.delete_user(id)
    return jsonify({'success': True})

    