import os

from celery.app import Celery
from decouple import config

env = config('DJANGO-ENV'.lower())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{env}')
app = Celery('chrona')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
