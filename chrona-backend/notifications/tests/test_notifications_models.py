import pytest
from datetime import timedelta
from django.utils import timezone
from notifications.models import PushSubscription
from users.tests.factories import UserFactory
from utils.orm import get_raw_column_value
from utils.shield import compute_hmac


@pytest.mark.django_db
def test_push_subscription_creation():
    user = UserFactory()
    subscription = PushSubscription.objects.create(
        user=user,
        endpoint='https://push.example.com/fake-subscription-id',
        expiration_time=timezone.now() + timedelta(days=1),
        p256dh='fake-public-key',
        auth='fake-auth-key'
    )

    assert PushSubscription.objects.count() == 1
    assert subscription.endpoint.startswith('https://push.example.com/')
    assert subscription.p256dh == 'fake-public-key'
    assert subscription.auth == 'fake-auth-key'
    assert str(subscription).startswith(f'PushSubscription(user={user.id}, endpoint=')


@pytest.mark.django_db
def test_safe_search_lookup():
    user = UserFactory()
    endpoint = 'https://push.example.com/abc123'
    PushSubscription.objects.create(
        user=user,
        endpoint=endpoint,
        p256dh='key1',
        auth='auth1'
    )

    # Lookup using HMAC should work
    result = PushSubscription.objects.get(endpoint=endpoint)
    assert result.user == user
    assert result.endpoint == endpoint


# @pytest.mark.django_db
# def test_endpoint_encryption_hmac_storage():
#     user = UserFactory()
#     endpoint = 'https://push.example.com/xyz987'
#     sub = PushSubscription.objects.create(
#         user=user,
#         endpoint=endpoint,
#         p256dh='key2',
#         auth='auth2'
#     )
#
#     # 🧠 Get raw DB values without triggering decryption
#     raw_encrypted_value = get_raw_column_value(PushSubscription, 'endpoint', sub.id)
#     encrypted_value = raw_encrypted_value['endpoint']
#     hmac_value = raw_encrypted_value['_endpoint_hmac']
#
#     assert encrypted_value != endpoint                    # 🔐 Confirm encrypted
#     assert hmac_value == compute_hmac(endpoint)           # ✅ HMAC matches
#     assert encrypted_value.startswith('gAAAA')                # 🔐 Fernet prefix