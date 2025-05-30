import json
import logging
from django.conf import settings
from pywebpush import webpush, WebPushException
from notifications.models import PushSubscription

logger = logging.getLogger(__name__)


def send_push_notification(user, title: str, body: str, url: str = '/') -> None:
    """
    Sends a Web Push Notification to all active subscriptions for a given user.

    Args:
        user (User): Django User instance to whom the notification is targeted.
        title (str): Title of the notification.
        body (str): Body text of the notification.
        url (str, optional): URL to open when the user clicks the notification. Defaults to "/".

    Behavior:
        - Iterates through all valid `PushSubscription` entries for the user.
        - Sends push using `pywebpush` with VAPID credentials.
        - Cleans up expired/invalid subscriptions (410/404 errors).
        - Logs all outcomes for monitoring or debugging.
    """
    subscriptions = PushSubscription.objects.filter(user=user)

    for sub in subscriptions:
        try:
            subscription_info = {
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            }

            payload = json.dumps({
                "title": title,
                "body": body,
                "url": url,
            })

            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=settings.VAPID_KEY,
                vapid_claims={
                    "sub": f"mailto:{settings.DEFAULT_FROM_EMAIL}",
                }
            )
            logger.info(f"[Push] Notification sent to {sub.endpoint[:40]}...")

        except WebPushException as e:
            logger.warning(f"[Push] Failed for {sub.endpoint[:40]}...: {e}")
            if "410" in str(e) or "404" in str(e):
                # Invalid subscription; remove it from DB
                sub.delete()

        except Exception as ex:
            logger.error(f"[Push] Unexpected error for {sub.endpoint[:40]}...: {ex}")
