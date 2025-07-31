from celery import current_app
from django.contrib.auth import get_user_model
from utils.orm import Model, models

User = get_user_model()


class TaskRegistry(Model):
    """
    Tracks Celery tasks scheduled by the system, allowing for lifecycle management,
    such as revoking pending tasks when timers are paused, reset, or cancelled.

    Fields:
        - task_id: Celery task UUID.
        - task_type: Logical type (email, push, etc.).
        - user: User associated with the task.
        - related_model: Model name the task is tied to (e.g., 'Timers').
        - related_obj_id: ID of the related model instance.
        - scheduled_time: When the task is expected to execute.
        - is_revoked: Whether this task has been revoked via Celery.
    """

    TASK_TYPES = (
        ('timer_complete_email', 'Timer Complete Email'),
        ('timer_push_notify', 'Timer Push Notification'),
    )

    task_id = models.CharField(max_length=255, unique=True)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_registry'
    )
    related_model = models.CharField(max_length=100)
    related_obj_id = models.CharField(max_length=255)
    scheduled_time = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)

    def revoke(self, terminate=False) -> None:
        """
        Revoke this Celery task from execution if it's still pending.

        Args:
            terminate (bool): Whether to forcibly terminate the task if it's running.
        """
        current_app.control.revoke(self.task_id, terminate=terminate)
        self.is_revoked = True
        self.save(update_fields=['is_revoked'])

    def __str__(self):
        return f"TaskRegistry({self.task_type} → {self.related_model}:{self.related_obj_id} @ {self.scheduled_time})"
