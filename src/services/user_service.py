from datetime import datetime
from flask_login import current_user
from models import db, User
from flask import request, current_app as app
from werkzeug.security import generate_password_hash


class UserService:

    @classmethod
    def create_user(cls, user):
        print("user: ", vars(user))
        try:
            if current_user is not None and current_user.is_authenticated:
                user.created_by = current_user.id
            else:
                user.created_by = 'system'
            hashed_password = generate_password_hash(user.password, method='pbkdf2:sha256')
            user.password = hashed_password  # Use the User object passed in as a parameter
            db.session.add(user)
            db.session.commit()
            return user.id
        except Exception as e:
            print("Error in create_user: ", e)  # Print the error message
            db.session.rollback()
            raise e
        
    @classmethod
    def get_all_users(cls):
        try:
            page = request.args.get('page', 1, type=int)
            sort = request.args.get('sort', 'id', type=str)
            order = request.args.get('order', 'asc', type=str)
            per_page = request.args.get('per_page', 5, type=str)
            per_page = int(per_page)

            return User.query.order_by(getattr(User, sort).asc() if order == 'asc' else getattr(User, sort).desc()).paginate(page=page, per_page=per_page)
        except Exception as e:
            raise e

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            return User.query.get(user_id)
        except Exception as e:
            raise e

    @classmethod
    def get_user_by_username(cls, user_name):
        try:
            return User.query.filter_by(user_name=user_name).first()
        except Exception as e:
            raise e

    @classmethod
    def update_user_password(cls,db, user):
        try:
            user_db = User.query.get(user.id)
            user_db.password = generate_password_hash(user.password, method='sha256')
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def update_user(cls, user_id):
        try:
            user = User.query.get(user_id)
            user.user_name = request.form['user_name'] if request.form['user_name'] not in ('', None) else user.user_name
            user.full_name = request.form['full_name'] if request.form['full_name'] not in ('', None) else user.full_name
            user.email = request.form['email'] if request.form['email'] not in ('', None) else user.email
            
            if 'role' in request.form:
                user.role = request.form['role']
            
            user.updated_at = datetime.now()
            user.updated_by = current_user.id

            if current_user.id == int(user_id) and request.form['password'] not in ('', None):
                user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

            db.session.commit()
            return user_id
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    def delete_user(cls,user_id):

        try:
            user = User.query.get(user_id)
            if user is not None:
                db.session.delete(user)
                db.session.commit()
            else:
                print(f"No user found with id {user_id}")
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def login(cls):
        try:
            print("request.form['user_name']: ", request.form['user_name'])
            user = User.query.filter_by(user_name=request.form['user_name']).first()
            print("user: ", user)
            if user and user.check_password(request.form['password']):
                return user                
        except Exception as e:
            raise e
        
    @classmethod
    def get_email_availability(cls, email):
        try:
            user = User.query.filter_by(email=email).first()
            if(user is None):
                return 'available'
            return 'exist'
        except Exception as e:
            raise e
        
    @classmethod
    def get_max_id(cls):
        try:
            user = User.query.order_by(User.id.desc()).first()
            if(user is None):
                return 0
            return user.id
        except Exception as e:
            raise e
        
    @classmethod
    def search_users(cls, term, page, per_page):
        try:
            users = []
            if term:
                users = User.query.filter((User.full_name.ilike(f"%{term}%")) | (User.user_name.ilike(f"%{term}%"))).paginate(page=page, per_page=per_page, error_out=False).items
            else: 
                users = User.query.paginate(page=page, per_page=per_page, error_out=False).items
            return users
        except Exception as e:
            app.logger.error(f"Error while searching users: {e}")
            raise e
