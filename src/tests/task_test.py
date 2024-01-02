from unittest.mock import patch
import pytest
from app import create_app
from extensions import db
from models import Task, User
from datetime import datetime



@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # use an in-memory SQLite database for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # create all tables in the database
            yield client
            db.drop_all() 
            # clean up after each test
@pytest.fixture
def mock_user():
    user = User(user_name='test_user', password='123', full_name='Test User', email='test@test.com', role='test', created_by='test_creator', created_at=datetime.utcnow())
    return user

@pytest.fixture
def mock_task(mock_user):
    task = Task(title='Test Task', description='Test Description', status='pending', user=mock_user, created_by=mock_user, updated_by=mock_user, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    return task

@pytest.fixture
def logged_in_client(client, mock_user):
    # Log in the user
    with patch('routes.main_routes.user_service.login', return_value=mock_user):
        client.post('/login', data={'user_name': 'test_user', 'password': '123'})
    return client

def test_get_task_as_json(logged_in_client, mock_user, mock_task):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()
    db.session.add(mock_task)
    db.session.commit()

    # Log in
    logged_in_client.post('/login', data=dict(
        user_name=mock_user.user_name,  # changed 'username' to 'user_name'
        password='123'
    ), follow_redirects=True)

    # Act
    response = logged_in_client.get(f'/task/{mock_task.id}/json')

    # Assert
    assert response.status_code == 200
    assert 'title' in response.get_json()
    assert 'description' in response.get_json()

def test_create_task(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()
    
    task_data = {
        'title': 'Test Task',
        'description': 'Test Description',
        'status': 'pending',
        'user': mock_user.id 
    }

    # Act
    response = logged_in_client.post('/task/create', data=task_data)

    # Assert
    assert response.status_code == 302  # The status code should be 302 if the user is redirected after creating a task
    
def test_update_task(logged_in_client, mock_task, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()
    db.session.add(mock_task)
    db.session.commit()
    update_data = {
        'title': 'Updated Task', 
        'description': 'Updated Description',
        'user': mock_user.id  # Add the 'user' key to the form data
    }

    # Act
    response = logged_in_client.post(f'/task/{mock_task.id}/update', data=update_data)

    # Assert
    assert response.status_code == 302  # The status code should be 302 if the user is redirected after updating the task

def test_delete_task(logged_in_client, mock_task, mock_user):
    # Arrange
    db.session.add(mock_user)  # Add the user instance to the session
    db.session.commit()
    db.session.add(mock_task)
    db.session.commit()

    # Act
    response = logged_in_client.delete(f'/task/{mock_task.id}/delete')

    # Assert
    assert response.status_code == 200
    assert Task.query.get(mock_task.id) is None
    