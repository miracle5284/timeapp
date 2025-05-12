# config/settings/prod.py

from .base import *

DEBUG = True


print(111, ALLOWED_HOSTS, BASE_DIR, CONFIG_DIR)
# settings.py
INSTALLED_APPS += ["django_extensions"]


# Production database config example (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST', default='localhost'),
        'PORT': config('POSTGRES_PORT', default='5432'),
    }
}

# Security
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# # Static and media
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
STATIC_DIR = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / STATIC_DIR,
    BASE_DIR / 'timer'/ 'static'
]
