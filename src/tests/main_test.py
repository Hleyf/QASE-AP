import pytest
from routes import main_routes as main
from app import create_app 
from models import User
from unittest import mock



@pytest.fixture
def client():
    app = create_app()  # create an instance of the application
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
@pytest.fixture
def test_user_created():
    test_user = User(
        user_name='test_user',
        password='123',
        full_name='Test User',
        role='user',
        email= 'test@mail.com'
    )
    response = main.main_routes.register(test_user)
    assert response.status_code == 200
    
        
def test_login_post_valid_credentials(client):
    valid_credentials = {'user_name': 'test_user', 'password': '123'}
    expected_redirect_location = '/home'
    
    test_user = User(user_name='test_user', password='123')
    with mock.patch('routes.main_routes.user_service.login', return_value=test_user):
        response = client.post('/login', data=valid_credentials)

    assert response.status_code == 302    
    assert response.location == expected_redirect_location

def test_login_post_invalid_credentials(client):
    invalid_credentials = {'user_name': 'invalid_user', 'password': 'invalid_password'}
    with mock.patch('routes.main_routes.user_service.login', return_value=None):
        response = client.post('/login', data=invalid_credentials)

    assert response.status_code == 200
    
def test_logout(client):
    # Log in a user
    test_user = User(user_name='test_user', password='123')
    with client.session_transaction() as session:
        session['user_id'] = test_user.id  # log in the user by storing their user ID in the session

    response = client.get('/logout')

    assert response.status_code == 302
    assert '/login' in response.location
    with client.session_transaction() as session:
        assert session.get('user_id') is None  # user should be logged out
