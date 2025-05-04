from rest_framework_simplejwt.tokens import RefreshToken
from social_core.pipeline.partial import partial

@partial
def issue_jwt_token(strategy, backend, user, *args, **kwargs):
    """Create JWT tokens for user that logged in using social auth"""
    
    # Generate token
    refresh = RefreshToken.for_user(user)
    
    # Store tokens in session
    strategy.session_set('jwt_access_token', str(refresh.access_token))
    strategy.session_set('jwt_refresh_token', str(refresh))
    
    return {
        'user': user,
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    } 