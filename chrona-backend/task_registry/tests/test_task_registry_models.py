import pytest
from unittest.mock import patch
from django.utils import timezone
from users.tests.factories import UserFactory
from task_registry.models import TaskRegistry
import uuid
from datetime import timedelta


@pytest.mark.django_db
def test_task_registry_creation():
    user = UserFactory()
    task = TaskRegistry.objects.create(
        task_id=str(uuid.uuid4()),
        task_type='timer_complete_email',
        user=user,
        related_model='Timers',
        related_obj_id='123',
        scheduled_time=timezone.now() + timedelta(minutes=5),
    )

    assert TaskRegistry.objects.count() == 1
    assert not task.is_revoked
    assert str(task) == f"TaskRegistry(timer_complete_email → Timers:123 @ {task.scheduled_time})"


@pytest.mark.django_db
@patch("celery.current_app.control.revoke")
def test_task_registry_revoke(mock_revoke):
    user = UserFactory()
    task = TaskRegistry.objects.create(
        task_id=str(uuid.uuid4()),
        task_type='timer_push_notify',
        user=user,
        related_model='Timers',
        related_obj_id='456',
        scheduled_time=timezone.now() + timedelta(minutes=10),
    )

    task.revoke(terminate=True)
    mock_revoke.assert_called_once_with(task.task_id, terminate=True)
    task.refresh_from_db()
    assert task.is_revoked is True
