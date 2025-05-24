import pytest

from users.serializers import RegisterUserSerializer, UserTokenSerializer, UserSerializer
from users.tests.factories import UserFactory, USER_TEST_PASSWORD


@pytest.mark.django_db
def test_register_user_serializer_valid():
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "StrongPass123",
        "confirm_password": "StrongPass123",
        "first_name": "John",
        "last_name": "Doe"
    }

    serializer = RegisterUserSerializer(data=data)

    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.email == data["email"]
    assert user.username == data["username"]
    assert user.check_password(data["password"])

@pytest.mark.django_db
def test_register_user_serializer_mismatch_passwords():
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "pass1",
        "confirm_password": "pass2",
        "first_name": "Jane",
        "last_name": "Doe"
    }

    serializer = RegisterUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'non_field_errors' in serializer.errors or 'Passwords do not match.' in str(serializer.errors)

@pytest.mark.django_db
def test_user_token_serializer_valid_credentials():
    user = UserFactory(password=USER_TEST_PASSWORD)
    data = {
        "email": user.email,
        "password": USER_TEST_PASSWORD
    }
    serializer = UserTokenSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data.get('access') is not None
    assert serializer.validated_data.get('refresh') is not None

@pytest.mark.django_db
def test_user_serializer_output():
    user = UserFactory()
    serializer = UserSerializer(user)
    data = serializer.data
    assert data.get('email') == user.email
    assert data.get('username') == user.username
    assert data.get('first_name') == user.first_name
    assert data.get('last_name') == user.last_name
    assert 'is_superuser' not in data
    assert 'password' not in data

