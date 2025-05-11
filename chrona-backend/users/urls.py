from django.urls import path

from .views import *
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('register', RegisterUserView.as_view(), name='register'),
    path('auth/token', UserTokenView.as_view(), name='auth-obtain-token'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='auth-refresh-token'),
    path('auth/token/verify', TokenVerifyView.as_view(), name='auth-verify-token'),
    path('logout', LogoutUserView.as_view(), name='logout'),
    path('password-reset', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path("", UserView.as_view(), name="get-user"),
    path('auth/social/login-url', SocialAuthURL.as_view(), name='social-login-url'),
    path('auth/oauth/tokens/', OAuth2TokenView.as_view(), name='oauth-token'),
]