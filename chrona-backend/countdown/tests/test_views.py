import time

import pytest
from django.urls import reverse
from django.utils import timezone

from countdown.models import Timers
from countdown.tests.factories import TimerFactory

TEST_TIMER_DURATION = 20
TEST_TIMER_SLEEP_DURATION = 5

@pytest.fixture
def timer(auth_client):
    client, user = auth_client
    return TimerFactory(user_id=user, name="Test Session", duration_seconds=TEST_TIMER_DURATION)

@pytest.mark.django_db
def test_create_timer(auth_client):
    client, user = auth_client
    url = reverse("timer-list")
    data = {"name": "Test Session", "duration_seconds": TEST_TIMER_DURATION, "timestamp": timezone.now().isoformat()}
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 201
    assert response.data["name"] == "Test Session"

    timer = Timers.objects.get(pk=response.data["id"])
    assert timer.user_id == user

@pytest.mark.django_db
def test_pause_timer(auth_client, timer):
    client, user = auth_client
    time.sleep(TEST_TIMER_SLEEP_DURATION)
    url = reverse("timer-pause", kwargs={"pk": timer.pk})
    response = client.patch(url, data={"timestamp": timezone.now().isoformat()}, content_type="application/json")
    assert response.status_code == 200
    assert response.data["status"] == "paused"

@pytest.mark.django_db
def test_start_timer(auth_client, timer):
    client, user = auth_client
    url = reverse("timer-start", kwargs={"pk": timer.pk})
    response = client.patch(url, data={
        "timestamp": timezone.now().isoformat(),
        "duration_seconds": TEST_TIMER_DURATION,
    }, content_type="application/json")
    assert response.status_code == 200
    assert response.data["status"] == "active"
    assert TEST_TIMER_DURATION - 2 < response.data["remaining_duration_seconds"] < TEST_TIMER_DURATION
    assert response.data["duration_seconds"] == TEST_TIMER_DURATION

@pytest.mark.django_db
def test_get_timer(auth_client, timer):
    client, user = auth_client
    time.sleep(TEST_TIMER_SLEEP_DURATION)
    get_url = reverse("timer-detail", kwargs={"pk": timer.pk})
    response = client.get(get_url)
    assert response.status_code == 200
    assert response.data["status"] == "pending"
    assert response.data["remaining_duration_seconds"] == 0
    assert response.data["duration_seconds"] == TEST_TIMER_DURATION

    patch_url = reverse("timer-start", kwargs={"pk": timer.pk})
    client.patch(patch_url, data={
        "timestamp": timezone.now().isoformat(),
        "duration_seconds": TEST_TIMER_DURATION,
    }, content_type="application/json")

    time.sleep(TEST_TIMER_SLEEP_DURATION)
    response = client.get(get_url)
    assert response.status_code == 200
    assert response.data["status"] == "active"
    assert (TEST_TIMER_DURATION - TEST_TIMER_SLEEP_DURATION - 2 < response.data["remaining_duration_seconds"] <=
            TEST_TIMER_DURATION - TEST_TIMER_SLEEP_DURATION)
    assert response.data["duration_seconds"] == TEST_TIMER_DURATION

@pytest.mark.django_db
def test_reset_timer(auth_client, timer):
    client, user = auth_client
    url = reverse("timer-reset", kwargs={"pk": timer.pk})
    response = client.patch(url, data={"timestamp": timezone.now().isoformat()}, content_type="application/json")
    assert response.status_code == 200
    assert response.data["status"] == "inactive"
    assert response.data["duration_seconds"] == TEST_TIMER_DURATION
    assert TEST_TIMER_DURATION - 2 < response.data["remaining_duration_seconds"] <= TEST_TIMER_DURATION
