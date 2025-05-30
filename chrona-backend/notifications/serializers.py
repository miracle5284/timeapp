from rest_framework import serializers
from notifications.models import PushSubscription


class PushSubscriptionSerializer(serializers.ModelSerializer):
    """
    Serializer for the PushSubscription model.

    This serializer handles serialization and deserialization of push subscription
    data, which is typically used for Web Push notifications (e.g., with VAPID + Service Worker).
    """

    # Uncomment below if you want to flatten nested "keys" dict into top-level fields:
    # p256dh = serializers.CharField(source='keys.p256dh', write_only=True)
    # auth = serializers.CharField(source='keys.auth', write_only=True)

    class Meta:
        model = PushSubscription
        fields = "__all__"