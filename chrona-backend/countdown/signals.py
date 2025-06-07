from datetime import timedelta

from celery import current_app
from django.db.models.signals import post_save
from django.utils.timezone import is_naive, make_aware
from django.dispatch import receiver

from notifications.tasks import push_user_timer_complete
from task_registry.models import TaskRegistry
from .models import Timers
from .tasks import send_timer_complete_email

GRACE_PERIOD = 10  # Extra buffer (in seconds) after timer completion before sending notifications

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

@receiver(pre_save, sender=Timers)
def timer_status(sender, instance, **kwargs):
    # TODO: Add unit test for presave and postw
    if instance.pk:
        try:
            instance._prev_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            instance._prev_instance = None
    else:
        instance._prev_instance = None

@receiver(post_save, sender=Timers)
def timer_status_watcher(sender, instance, created, **kwargs):
    """
    Signal handler to monitor timer status changes and schedule or revoke Celery tasks accordingly.

    If a timer is activated (`status == 'active'`), this schedules:
        - An email notification (`send_timer_complete_email`)
        - A push notification (`push_user_timer_complete`)

    If the timer is paused, completed, or reset (`status != 'active'`), previously scheduled tasks are revoked.

    Args:
        sender (Model): The model class (Timers).
        instance (Timers): The actual instance being saved.
        created (bool): Whether this is a new instance.
        **kwargs: Extra keyword arguments.
    """

    scheduled_tasks = []
    prev_status = None
    if not created and hasattr(instance, '_prev_instance') and instance._prev_instance:
        prev_status = instance._prev_instance.status
    if instance.is_active and instance.resumed_at:
        if instance.user_id and instance.user_id.email:
            # Calculate the exact notification time
            scheduled_time = instance.resumed_at + timedelta(
                seconds=instance.remaining_duration_seconds + GRACE_PERIOD
            )

            # Ensure datetime is timezone-aware
            if is_naive(scheduled_time):
                scheduled_time = make_aware(scheduled_time)

            # Schedule the email notification
            email_task = send_timer_complete_email.apply_async(
                args=[instance.user_id.email, instance.id],
                eta=scheduled_time
            )
            scheduled_tasks.append(TaskRegistry(
                task_id=email_task.id,
                task_type='timer_complete_email',
                user=instance.user_id,
                related_model=instance.__class__.__name__,
                related_obj_id=instance.id,
                scheduled_time=scheduled_time
            ))

            # Schedule the push notification
            push_task = push_user_timer_complete.apply_async(
                args=[instance.user_id.id, instance.id],
                eta=scheduled_time
            )
            scheduled_tasks.append(TaskRegistry(
                task_id=push_task.id,
                task_type='timer_push_notify',
                user=instance.user_id,
                related_model=instance.__class__.__name__,
                related_obj_id=instance.id,
                scheduled_time=scheduled_time
            ))

            # Save both scheduled tasks to the DB
            TaskRegistry.objects.bulk_create(scheduled_tasks)

    # elif prev_status == 'active' and not instance.is_active:
    elif instance.status not in ('active', 'completed'):
        # If the timer is paused/completed/reset, revoke any existing tasks
        for task in TaskRegistry.objects.filter(
            related_model=instance.__class__.__name__,
            related_obj_id=instance.id,
            is_revoked=False,
            task_type__in=['timer_push_notify', 'timer_complete_email']
        ):
            current_app.control.revoke(task.task_id, terminate=True)
            task.is_revoked = True
            task.save()
