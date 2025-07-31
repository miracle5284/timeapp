from celery import shared_task
from django.contrib.auth import get_user_model

from .services import send_push_notification


@shared_task(name="push_user_timer_complete")
def push_user_timer_complete(user_id: int, timer_name: str = None) -> None:
    """
    Celery task to send a push notification to a user when their timer completes.

    Args:
        user_id (int): ID of the target user.
        timer_name (str, optional): Name of the timer for contextual messaging.
    """
    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # User no longer exists, silently exit
        return

    title = "Chrona: Timer Finished"
    body = f"'{timer_name}' has ended!" if timer_name else "Your timer is complete."
    url = "/dashboard"

    # Call the service that wraps pywebpush
    try:
        send_push_notification(user, title, body, url)
    except Exception as e:
        # TODO:
        # Let Celery retry on failure if configured
        raise e
