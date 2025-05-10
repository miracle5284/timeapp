from corsheaders.defaults import default_headers
from decouple import config

SESSION_COOKIE_SECURE       = True
SESSION_ENGINE              = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME         = 'sessionid'
SESSION_COOKIE_HTTPONLY     = True   # JS can’t read sessionid
CSRF_COOKIE_SAMESITE        = 'Strict'
SESSION_COOKIE_SAMESITE      = 'Strict'

CHRONA_SESSION_COOKIE_NAME = 'chrona_oauth_sessionid'



CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS').split(',')
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    'authorization', 'content-type'
]
CORS_ALLOWED_CREDENTIALS = True
CORS_PREFLIGHT_MAX_AGE = 86400

CSRF_TRUSTED_ORIGINS = config('CORS_ALLOWED_ORIGINS').split(',')
