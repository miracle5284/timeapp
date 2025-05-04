"""
WSGI config for zeero project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from decouple import config
from django.core.wsgi import get_wsgi_application

print("QQQQQQ: ", os.environ)
env = config('DJANGO-ENV'.lower(), default='prod')
print('Django ENVVV: ', env)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{env}')

application = get_wsgi_application()
