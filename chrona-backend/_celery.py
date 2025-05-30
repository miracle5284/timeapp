import os

from celery.app import Celery
from decouple import config

env = config('DJANGO_ENV')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{env}')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('chrona')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


__all__ = ['app']
