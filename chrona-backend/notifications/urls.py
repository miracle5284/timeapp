# urls.py
from django.urls import path
from notifications.views import PushSubscriptionView

urlpatterns = [
    path('subscribe', PushSubscriptionView.as_view(), name='push-subscribe'),
]
