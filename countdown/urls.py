from django.urls import path
from countdown.views import CountDownView

urlpatterns = [
    path('', CountDownView.as_view(), name='countdown'),
]