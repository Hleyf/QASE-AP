# Creates the initial admin user 
from datetime import datetime
from models import db
from werkzeug.security import generate_password_hash
from models import User
from faker import Faker

def create_admin():
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

def create_users():
    previous_users = User.query.all()
    if len(previous_users) <= 1:
        fake = Faker()
        # generate 30 random users and adds them to the database
        for i in range(30):
            user = User(
                user_name=f'user{i}',
                email=fake.email(),
                password='123',
                full_name=fake.name() + ' ' + fake.last_name(),
                role='user',
                created_at=datetime.now(),
                created_by='system'
            )
            hashed_password = generate_password_hash(user.password, method='pbkdf2:sha256')
            user.password = hashed_password
            db.session.add(user)
        db.session.commit()