import os

from celery.app import Celery
from decouple import config

env = config('DJANGO_ENV')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{env}')
# os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('chrona')
#
# app.conf.broker_url = settings.CELERY_BROKER
# app.conf.broker_use_ssl = {
#     "ssl_cert_reqs": ssl.CERT_NONE,
# }
# TODO: Remove on switching to rabbitmq
app.conf.broker_transport_options = {
    "visibility_timeout": 3600,  # optional
    "socket_timeout": 30,        # increase socket timeout to reduce need for PING
    "retry_on_timeout": True,
}
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


__all__ = ['app']
