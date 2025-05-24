import subprocess

import pytest
import django
from django.conf import settings
from django.core.cache import cache
from rest_framework.test import APIClient
from users.tests.factories import UserFactory, USER_TEST_PASSWORD

settings.SECURE_SSL_REDIRECT = False

django.setup()


@pytest.fixture
def auth_client(db):
    user = UserFactory(password=USER_TEST_PASSWORD)
    client = APIClient()

    response = client.post("/users/auth/token", {
        "email": user.email,
        "password": "testPass@123"
    })
    print("Login response code:", response.status_code)
    print("Login response headers:", response.headers)
    print("Login response content:", response.content)
    print("SSL REDIRECT ENABLED?", settings.SECURE_SSL_REDIRECT)
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client, user

# TODO: handle 429 realistically test
@pytest.fixture(autouse=True)
def clear_throttle_cache():
    cache.clear()

def pytest_sessionfinish(session, exitstatus):
    if exitstatus != 0:
        return

    result = subprocess.run(["coverage", "report"], capture_output=True, text=True)

    print(result.stdout)

    total_coverage = None
    for line in result.stdout.strip().splitlines():
        if 'TOTAL' in line:
            try:
                total_coverage = int(line.split()[-1].strip('%'))
                break
            except (ValueError, IndexError):
                pass
    if total_coverage is None:
        print("❌ Could not determine total coverage")
        session.exitstatus = 1
        return

    if total_coverage < 80:
        print(f"❌ Coverage is too low: {total_coverage}% < 80% — failing test run.")
        session.exitstatus = 1

    elif total_coverage < 90:
        print(f"⚠️ Warning: Coverage below 90% — currently at {total_coverage}%.")

    else:
        print(f"✅ Coverage is healthy: {total_coverage}%")
