import pytest
from app import create_app
from extensions import db
from models import User
from datetime import datetime
from flask_login import login_user
from unittest.mock import patch


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # use an in-memory SQLite database for testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # create all tables in the database
            yield client
            db.drop_all()  # clean up after each test

@pytest.fixture
def mock_user():
    user = User(user_name='test_user', password='123', full_name='Test User', email='test@test.com', role='test', created_by='test_creator', created_at=datetime.utcnow())
    return user

@pytest.fixture
def logged_in_client(client, mock_user):
    # Log in the user
    with patch('routes.main_routes.user_service.login', return_value=mock_user):
        client.post('/login', data={'user_name': 'test_user', 'password': '123'})
    return client

def test_get_all_users(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()

    # Act
    response = logged_in_client.get('/users')

    # Assert
    assert response.status_code == 200
    
def test_get_user_as_json(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()


    # Act
    response = logged_in_client.get(f'/user/{mock_user.id}/json')

    # Assert
    assert response.status_code == 200
    user_dict = mock_user.to_dict()
    user_dict['created_at'] = user_dict['created_at'].strftime('%a, %d %b %Y %H:%M:%S GMT')
    assert response.get_json() == user_dict


def test_check_email_availability_free(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()

    # Act
    response = logged_in_client.get(f'/user/available@email.com')

    # Assert
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'available'


def test_check_email_availability_taken(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()

    # Act
    response = logged_in_client.get(f'/user/{mock_user.email}')

    # Assert
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'exist'
    
def test_delete_user(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()


    # Act
    response = logged_in_client.delete(f'/users/{mock_user.id}/delete')

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {'success': True}

def test_current_user_role(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()


    # Act
    response = logged_in_client.get('/current_user_role_info')

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {'id': mock_user.id, 'role': mock_user.role}
    
def test_search_users(logged_in_client, mock_user):
    # Arrange
    db.session.add(mock_user)
    db.session.commit()


    # Mock the search_users function to return the mock_user
    with patch('routes.user_routes.service.search_users', return_value=[mock_user]):
        # Act
        response = logged_in_client.get('/users/search?q=test')

    # Convert datetime to string in ISO 8601 format for the expected response
    mock_user_dict = mock_user.to_dict()
    mock_user_dict['created_at'] = mock_user_dict['created_at'].strftime('%a, %d %b %Y %H:%M:%S GMT')

    # Assert
    assert response.status_code == 200
    assert response.get_json() == {'items': [mock_user_dict]}
