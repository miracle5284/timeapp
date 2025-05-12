from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from social_core.backends.google import GoogleOAuth2


class SecureGoogleOAuth2(GoogleOAuth2):
    """
    Custom Google OAuth2 backend that:
    - Creates an isolated session for the OAuth flow (separate from user's main session)
    - Attaches the session manually to the strategy and request
    - Issues a secure SameSite=None cookie for cross-origin OAuth popup flow
    """

    def get_redirect_uri(self, state=None):
        """
        Override the redirect URI generation to ensure the session is saved before continuing.

        This prevents 'Session value state missing' errors caused by unsaved sessions
        when Google redirects back to the completion URL.
        """
        if not self.strategy.session.session_key:
            self.strategy.session.save()

        return super().get_redirect_uri(state)

    def start(self):
        """
        Starts the OAuth authorization by:

        1. Creating a fresh, backend-isolated session using SessionStore
        2. Manually assigning it to the strategy and the request
        3. Setting a secure cookie manually to support cross-site for the auth purpose.
        4. Delegating to the default start logic of the GoogleOAuth2 backend

        This ensures compatibility with cross-origin popups and session-scoped OAuth flow.
        """

        # Create a new backend session and persist it
        session = SessionStore()
        session.save()

        # Inject session into strategy and request (used internally by social-auth)
        self.strategy.session = session
        self.strategy.request.session = session

        # Begin the standard OAuth2 authorization flow
        response = super().start()

        # Manually set the session cookie with cross-origin compatibility
        response.set_cookie(
            key=settings.CHRONA_SESSION_COOKIE_NAME,
            value=session.session_key,
            secure=True,
            httponly=True,
            samesite='None',
            path='/',
            domain=None  # Defaults to the current domain; override if needed
        )

        return response
