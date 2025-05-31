import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.tests.factories import UserFactory, USER_TEST_PASSWORD


@pytest.mark.django_db
def test_user_registration():
    url = reverse('register')
    data = {
        "email": "new@example.com",
        "username": "newuser",
        "password": "Password123!",
        "confirm_password": "Password123!",
        "first_name": "Test",
        "last_name": "User"
    }

    response = APIClient().post(url, data, format='json')
    print('REGISTER URL: ', url, response.status_code, response.data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_token_login_success():
    user = UserFactory()
    url = reverse('auth-obtain-token')
    data = {
        "email": user.email,
        "password": USER_TEST_PASSWORD
    }

    response = APIClient().post(url, data, format='json')
    print('TEST URL: ', url, response.status_code, response.data)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_token_login_failure():
    user = UserFactory()
    url = reverse('auth-obtain-token')
    data = {
        "email": user.email,
        "password": "wrongPassword"
    }

    response = APIClient().post(url, data, format='json')
    assert response.status_code == 401
    assert 'access' not in response.data
    assert 'refresh' not in response.data
    assert response.data['detail'] == 'No active account found with the given credentials'

@pytest.mark.django_db
def test_get_current_user(auth_client):
    client, user = auth_client
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.data['results'][0]['email'] == user.email
    assert response.data['results'][0]['username'] == user.username

@pytest.mark.django_db
def test_logout(auth_client):
    client, user = auth_client
    url = reverse('logout')
    refresh = str(RefreshToken.for_user(user))
    response = client.post(url, {'refresh': refresh}, format='json')
    assert response.status_code == 205
    assert response.data['detail'] == 'Logout successful'

    response = client.get('/users/')
    assert response.status_code == 401


@pytest.mark.django_db
def test_social_auth_url():
    url = reverse('social-login-url') + '?provider=google'
    response = APIClient().get(url)
    assert response.status_code == 200
    assert 'login_url' in response.data

@pytest.mark.django_db
def test_oauth_token_view(auth_client):
    client, user = auth_client
    url = reverse('oauth-token')
    response = client.get(url)
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
