from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from django.conf import settings
from utils.views import BaseCreateAPIView, BaseGenericAPIView, BaseListUpdateAPIView, BaseAPIView
from .serializers import UserTokenSerializer, UserSerializer

from .serializers import RegisterUserSerializer


User = get_user_model()


class RegisterUserView(BaseCreateAPIView):
    """
    API view to register a new user.
    """

    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

class LogoutUserView(BaseGenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserTokenView(TokenObtainPairView):

    serializer_class = UserTokenSerializer


class PasswordResetRequestView(BaseGenericAPIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': "if this email exist, a reset link has been sent"}, status=status.HTTP_200_OK)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{request.data.get('redirect_base_url')}?uid={uid}&token={token}"

        send_mail(
            subject='Password Reset Request',
            message=f'Click the link to reset your password: {reset_link}',
            recipient_list=[email],
        )

        return Response({'detail': "if this email exist, a reset link has been sent"}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(BaseGenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uid64 = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        if password != confirm_password:
            return Response({'detail': "passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = force_str(urlsafe_base64_encode(uid64))
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return Response({'detail': "invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'detail': "Reset link is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password, user=user)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'detail': "Password reset successful"}, status=status.HTTP_200_OK)


class UserView(BaseListUpdateAPIView):
    """
    API view to retrieve, update or delete a user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_object(self):
        return self.request.user


class SocialAuthURL(BaseAPIView):
    """
    Returns the OAuth login URL for a given social provider.

    This endpoint is called by the frontend to obtain the `begin` URL
    from `python-social-auth`, e.g., /auth/login/google-oauth2/.
    """

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        provider = request.query_params.get('provider')
        backend = settings.BACKEND_MAP.get(provider)

        if not backend:
            return Response({'detail': 'Invalid provider'}, status=status.HTTP_400_BAD_REQUEST)

        login_path = reverse('social:begin', args=[backend])
        login_url = request.build_absolute_uri(login_path)

        return Response({'login_url': login_url}, status=status.HTTP_200_OK)


class OAuth2TokenView(BaseAPIView):
    """
    Called from the OAuth popup window after social-auth login completes.

    Assumes a valid session has already authenticated the user (e.g., via
    Django session auth middleware). Returns JWT access and refresh tokens
    for frontend use.
    """

    permission_classes = [IsAuthenticated]  # Should protect this view!

    def get(self, request, *args, **kwargs):
        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'success': True,
            'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_200_OK)
