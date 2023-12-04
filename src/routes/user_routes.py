from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from services import UserService



user_routes = Blueprint('user_routes', __name__)
service = UserService()

@user_routes.route('/users')
@login_required
def users():
    users = service.get_all_users()
    is_admin = current_user.role == 'admin'

    return render_template('pages/user_list.html', users=users, is_admin=is_admin, logged_user_id=current_user.id)


#Get method to return user.id by email
@user_routes.route('/user/<email>', methods=['GET'])
@login_required
def check_email_availability(email):
    response = service.get_email_availability(email)
    return response

@user_routes.route('/users/<id>/edit', methods=['GET','POST'])
@login_required
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
        
@user_routes.route('/users/<id>/delete', methods=['DELETE'])
@login_required
def delete_user(id):
    UserService.delete_user(id)
    return jsonify({'success': True})