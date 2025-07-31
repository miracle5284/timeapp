from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication as JWT_AUTH
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import AccessToken, Token


class BaseJWTAuthentication(JWT_AUTH):

    pass


class BlacklistAwareJWTAuthentication(BaseJWTAuthentication):

    def get_validated_token(self, raw_token: bytes) -> Token:
        token = super().get_validated_token(raw_token)

        if isinstance(token, AccessToken):
            jti = token.get('jti')
            try:
                token_obj = OutstandingToken.objects.get(jti=jti)
                if BlacklistedToken.objects.filter(token__jti=jti).exists():
                    raise exceptions.AuthenticationFailed("Token is blacklisted", code="token_blacklisted")
            except OutstandingToken.DoesNotExist:
                pass

        return token


class JWTAuthentication(BlacklistAwareJWTAuthentication):

    pass