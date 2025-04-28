from django.urls import path
from . import api_views

urlpatterns = [
    path('health/', api_views.health_check, name='health_check'),
    path('extension-info', api_views.extension_info, name="extension-info"),
]