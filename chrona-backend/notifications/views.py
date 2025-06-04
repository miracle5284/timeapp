from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from notifications.serializers import PushSubscriptionSerializer, PushSubscription
from utils.views import BaseAPIView


class PushSubscriptionView(BaseAPIView):
    """
    Handles registration of a Web Push subscription from an authenticated client.

    Accepts a POST request with a browser push subscription object,
    extracts and saves the `endpoint`, `p256dh`, and `auth` values
    in the encrypted PushSubscription model.

    Expected input format:
    {
        "endpoint": "...",
        "expirationTime": "...",  # optional
        "keys": {
            "p256dh": "...",
            "auth": "..."
        }
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data.copy()

        # Flatten nested keys structure for serializer compatibility
        data['user'] = user.id
        data['p256dh'] = data.get('keys', {}).get('p256dh')
        data['auth'] = data.get('keys', {}).get('auth')

        status, _ = PushSubscription.objects.create_or_update(
            user=user.id,
            endpoint=data.get('endpoint'),
            defaults={
                    'expiration_time': data.get('expiration_time'),
                    'p256dh': data['p256dh'],
                    'auth': data['auth'],
                },
            serializer_cls=PushSubscriptionSerializer,
        )

        return Response({'status': 'subscription %s successfully.' % (status and 'created' or 'updated')})
