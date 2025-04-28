from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('set_timer', views.set_timer, name='set_timer'),
    path('reset_timer', views.reset_timer, name='reset_timer'),
    path('pause_timer', views.pause_timer, name='pause_timer'),
]