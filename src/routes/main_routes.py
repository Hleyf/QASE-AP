from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from flask_login import login_required, current_user, login_user, logout_user
from models import User
from services import UserService


main_routes = Blueprint('main', __name__)
user_service = UserService()

@main_routes.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('main.login'))        
    else:
        return redirect(url_for('main.home'))

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = user_service.login()
        if user:
            login_user(user)
            return redirect(url_for('main.home'))            
        else:
            return render_template('auth/login.html', error="Invalid credentials")
    elif request.method == 'GET' and 'user' not in session:
        return render_template('auth/login.html')
    elif request.method == 'GET' and 'user' in session:
        return redirect(url_for('main.home'))

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_user = User(
            user_name=request.form['user_name'],
            password=request.form['password'],
            full_name=request.form['full_name'],
            email=request.form['email'],
            role=request.form['role'] if 'role' in request.form else 'user',
            created_at=datetime.now(),
            created_by= None
        )
        with current_app.app_context():
            user_id = user_service.create_user(form_user)
        
        if not user_id:
            return render_template('auth/register.html', error="Invalid credentials")

        return redirect(url_for('user_routes.users')) if current_user.is_authenticated else redirect(url_for('main.login'))
    is_admin = current_user is not None and current_user.is_authenticated and current_user.role == 'admin'
    return render_template('auth/register.html', is_admin=is_admin)

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_routes.route('/home')
@login_required
def home():
    return render_template('pages/home.html')


    




    