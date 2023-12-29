from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from services import UserService



user_routes = Blueprint('user_routes', __name__)
service = UserService()

@user_routes.route('/users')
@login_required
def users():
    users = service.get_all_users()
    is_admin = current_user.role == 'admin'

    return render_template('pages/user_list.html', users=users, is_admin=is_admin, logged_user_id=current_user.id)

@user_routes.route('/users/<id>/json', methods=['GET'])
@login_required
def get_user_as_json(id):
    user = service.get_user_by_id(int(id))
    return jsonify(user.to_dict())

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

@user_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@user_routes.route('/current_user_role_info')
def current_user_role():
    if current_user.is_authenticated:
        # return an object with two properties: id and role
        return jsonify({'id': current_user.id, 'role': current_user.role})
    else:
        return "User not authenticated"