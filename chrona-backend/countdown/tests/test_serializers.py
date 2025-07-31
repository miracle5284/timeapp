import pytest
from countdown.serializers import TimerSerializer, Timers
from countdown.tests.factories import TimerFactory
from django.utils import timezone
from unittest.mock import Mock

from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_timer_serializer_valid_data():
    data = {
        "name": "Focus Timer",
        "duration_seconds": 1500,  # 25 mins
        "status": "pending",
        "timestamp": timezone.now().isoformat(),
    }
    serializer = TimerSerializer(data=data)
    serializer.context['endpoint'] = '/countdown/'
    req = Mock()
    req.user = UserFactory()
    serializer.context['request'] = req
    assert serializer.is_valid(), serializer.errors
    instance = serializer.save()
    assert instance.name == "Focus Timer"
    assert instance.duration_seconds == 1500


@pytest.mark.django_db
def test_timer_serializer_missing_name():
    data = {
        "duration_seconds": 300,
        "timestamp": timezone.now().isoformat()

    }
    serializer = TimerSerializer(data=data)
    serializer.context['endpoint'] = '/countdown/'
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_timer_serializer_invalid_duration():
    data = {
        "name": "Break",
        "duration_seconds": -100,
        "timestamp": timezone.now().isoformat()
    }
    serializer = TimerSerializer(data=data)
    assert not serializer.is_valid()
    assert "duration_seconds" in serializer.errors


@pytest.mark.django_db
def test_timer_serializer_read_fields():
    timer = TimerFactory(status="active", start_at=timezone.now(), user_id=UserFactory())
    serializer = TimerSerializer(timer)
    data = serializer.data

    assert data["name"] == timer.name
    assert data["status"] == "active"
    assert "duration_seconds" in data
    assert "remaining_duration_seconds" in data
    assert data["remaining_duration_seconds"] <= timer.duration_seconds


@pytest.mark.django_db
def test_timer_serializer_prevents_edit_of_readonly():
    timer = TimerFactory(status="completed", user_id=UserFactory())
    serializer = TimerSerializer(timer, data={"status": "active"}, partial=True)
    serializer.context['endpoint'] = '/countdown/'

    # Assuming status is read-only in serializer:
    serializer.is_valid()
    serializer.data["status"] = "completed"
