# config/settings/prod.py

from .base import *

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
# CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
# CORS_ALLOWED_ORIGINS = ALLOWED_HOSTS

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

# # Storage
# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#     },
#
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
#         "AWS_S3_OBJECT_PARAMETERS": {
#             "CacheControl": "max-age=86400",
#         },
#     },
# }


# Security
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


STATICFILES_DIRS = []
timer_static = BASE_DIR / 'chrona' / 'static'
if timer_static.exists():
    STATICFILES_DIRS.append(timer_static)

REDIS_HOST = config('REDIS_HOST', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
    },

    'handlers': {
        'redis': {
            'level': LOG_LEVEL,
            'class': 'config.logging_handlers.RedisStreamHandler',
            'formatter': 'json',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',  # or 'json' if you want JSON logs in console too
        }

    },

    'root': {
        'handlers': ['console', 'redis'],
        'level': LOG_LEVEL,
    },

    'loggers': {
        'django': {
            'handlers': ['redis', 'console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'django.request': {
            'handlers': ['redis', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

