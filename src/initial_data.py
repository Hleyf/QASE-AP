# Creates the initial admin user 
from datetime import datetime
from models import db
from werkzeug.security import generate_password_hash



def create_admin():
    from models import User
    admin = User.query.filter_by(email='admin@admin.com').first()
    if admin is None:
        user = User(
            user_name='admin',
            email='admin@admin.com',
            password='admin',
            full_name='Administrator',
            role='admin',
            created_at=datetime.now(),
            created_by='system'
        )
    
        hashed_password = generate_password_hash(user.password, method='pbkdf2:sha256')
        user.password = hashed_password  # Use the User object passed in as a parameter
        db.session.add(user)
        db.session.commit()