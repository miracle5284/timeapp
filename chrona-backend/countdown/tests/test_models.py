import pytest
from countdown.models import Timers
from users.tests.factories import UserFactory
from .factories import TimerFactory, TEST_DURATION
from django.utils import timezone
from datetime import timedelta


@pytest.mark.django_db
def test_timer_factory_basics():
    user = UserFactory()
    timer = TimerFactory(user_id=user)
    assert isinstance(timer, Timers)
    assert timer.name  is not None
    assert timer.duration_seconds == TEST_DURATION
    assert timer.remaining_duration_seconds == 0
    assert timer.status == 'pending'
    assert timer.is_recurring == False
    assert timer.start_at is None
    assert timer.paused_at is None
    assert timer.resumed_at is None

@pytest.mark.django_db
def test_timer_factory_started_state():
    now = timezone.now()
    user = UserFactory()
    timer = TimerFactory(
        status='active',
        start_at=now,
        user_id=user
    )
    assert timer.name  is not None
    assert timer.duration_seconds == TEST_DURATION
    assert timer.remaining_duration_seconds == 0
    assert timer.status == 'active'
    assert timer.is_recurring == False
    assert timer.start_at == now
    assert timer.paused_at is None
    assert timer.resumed_at is None

@pytest.mark.django_db
def test_remaining_duration_countdown():
    now = timezone.now()
    user = UserFactory()
    start_at = now - timedelta(seconds=45)
    timer = TimerFactory(
        status="started",
        start_at=start_at,
        duration_seconds=100,
        user_id=user
    )

    assert timer.remaining_duration_seconds <= 55