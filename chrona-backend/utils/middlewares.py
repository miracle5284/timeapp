from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpResponseRedirect


class SmartSessionMiddleware(SessionMiddleware):
    """
    Middleware that intelligently switches between Chrona's custom session cookie
    and Django's default session cookie, depending on whether a custom session is present.

    This is primarily used to support secure, isolated sessions during OAuth flows.
    """

    def process_request(self, request):
        """
        If a custom Chrona session cookie is found, use it to initialize the session.
        Otherwise, fall back to Django's default session processing.
        """
        custom_cookie = request.COOKIES.get(settings.CHRONA_SESSION_COOKIE_NAME)
        if custom_cookie:
            request.session = SessionStore(session_key=custom_cookie)
            request._using_custom_session = True  # Track that we're using a custom session
        else:
            super().process_request(request)

    def process_response(self, request, response):
        """
        Handles session persistence and cookie logic on response.

        - If this is a redirect to the post-login redirect URL, persist the custom session.
        - If using a custom session but no session key exists, save it.
        - Avoid rewriting session unnecessarily by marking it as not modified.
        """
        is_oauth_redirect = (
            isinstance(response, HttpResponseRedirect)
            and response.get("Location") == settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL
        )

        if is_oauth_redirect:
            # Write back the Chrona session cookie after OAuth completes
            response.set_cookie(
                key=settings.CHRONA_SESSION_COOKIE_NAME,
                value=request.session.session_key,
                max_age=settings.SESSION_COOKIE_AGE,
                secure=True,
                httponly=True,
                samesite='None',
                path='/',
                domain=None  # You can set to `.chrona.com` if needed
            )

            # Persist the session and avoid rewriting on Django's side
            request.session.save()
            request.session.modified = False

        elif getattr(request, "_using_custom_session", False):
            # If using a Chrona session, and it's not saved yet — save it
            if not request.session.session_key:
                request.session.save()

        return super().process_response(request, response)
