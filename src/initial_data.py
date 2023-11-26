# Creates the initial admin user 
from datetime import datetime


def create_admin():
    from models import User
    from services import UserService
    user = User(
        user_name='admin',
        email='admin@admin.com',
        password='admin',
        full_name='Administrator',
        role='admin',
        created_at=datetime.now(),
        created_by=1
    )
    UserService.create_user(user)