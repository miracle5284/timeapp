import pytest
from users.tests.factories import UserFactory, USER_TEST_PASSWORD


@pytest.mark.django_db
def test_user_model():
    user = UserFactory()
    assert user.pk is not None
    assert  user.email is not None
    assert user.check_password(USER_TEST_PASSWORD)

    # Should not store plain password
    assert USER_TEST_PASSWORD not in user.password

