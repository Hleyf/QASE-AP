# Creates the initial admin user 
from datetime import datetime
from models import db
from werkzeug.security import generate_password_hash
from models import User, Task
from faker import Faker
from services import UserService

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
        
def create_tasks():
    if not len(Task.query.all()) == 0:
        return  # if there are tasks in the database, it does not create new ones
    max_id = UserService.get_max_id()
    if max_id == 0:
        raise Exception("No users found in the database")
    
    fake = Faker()
    # generate 30 random tasks and adds them to the database
    for i in range(30):
        # generates a random user id between 1 and the max id in the database
        user_id = fake.random_int(min=1, max=max_id)
        # looks for the user with the generated id
        user = User.query.get(user_id)
        # while the user is None, it generates a new id. This is to avoid the case where the user with the generated id was deleted
        while user is None:
            user_id = fake.random_int(min=1, max=max_id)
            user = User.query.get(user_id)
        # creates the task with the user found
        task = Task(
            title=fake.sentence(),
            description=fake.text(),
            status='pending',
            created_by=user,  
            created_at=datetime.now(),
        )
        db.session.add(task)
    db.session.commit()