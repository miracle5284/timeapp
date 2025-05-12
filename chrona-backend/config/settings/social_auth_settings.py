from datetime import timedelta

from decouple import config

from . import BASE_URL, FRONTEND_URL

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("SOCIAL_AUTH_GOOGLE_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'prompt': 'consent'
}

# Redirect URIs
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = '%s/auth/complete/google-oauth2/' % BASE_URL
SOCIAL_AUTH_ALLOWED_REDIRECT_URIS = [
    '%s/auth/complete/google-oauth2/' % BASE_URL,
]

SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [
    'first_name',
    'last_name',
    'picture',     # URL to the profile image
]

# Session settings for social auth
SOCIAL_AUTH_SESSION_COOKIE = 'social-auth'
SOCIAL_AUTH_STORAGE = 'social_django.models.DjangoStorage'
SOCIAL_AUTH_STRATEGY = 'social_django.strategy.DjangoStrategy'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '%s/oauth/popup' % FRONTEND_URL
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
# SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# JWT Settings for social auth
SOCIAL_AUTH_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# State parameter settings
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['state']
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    #'users.pipeline.jwt_popup_redirect',
)

BACKEND_MAP = {
    'google': 'google-oauth2',
    'facebook': 'facebook',
    'github': 'github',
    'linkedin': 'linkedin-oauth2',
}
