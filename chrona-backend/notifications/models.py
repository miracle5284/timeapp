from django.contrib.auth import get_user_model
from utils.orm import Model, models, EncryptedTextField

User = get_user_model()


class PushSubscription(Model):
    """
    Model to store Web Push subscription details for a user.

    Fields:
        - user: The user this subscription belongs to.
        - endpoint: Unique endpoint URL provided by the browser's push service.
        - expiration_time: Optional expiration timestamp for the subscription.
        - p256dh: Public encryption key (client-side) – encrypted at rest.
        - auth: Auth secret used for Web Push protocol – encrypted at rest.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='push_subscriptions'
    )
    endpoint = EncryptedTextField(unique=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    p256dh = EncryptedTextField(max_length=255)
    auth = EncryptedTextField(max_length=255)

    class Meta:
        safe_search_fields = ['endpoint']

    def __str__(self):
        return f'PushSubscription(user={self.user_id}, endpoint={self.endpoint[:40]}...)'
