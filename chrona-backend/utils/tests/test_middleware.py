import pytest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponseRedirect
from django.test import RequestFactory

from utils.middlewares import SmartSessionMiddleware


@pytest.mark.django_db
def test_custom_session_cookie(monkeypatch):
    factory = RequestFactory()
    request = factory.get('/')
    monkeypatch.setattr(settings, "CHRONA_SESSION_COOKIE_NAME", "chrona-sessionid")
    request.COOKIES["chrona-sessionid"] = "mock-session"

    middleware = SmartSessionMiddleware(get_response=lambda r: HttpResponseRedirect('/auth-complete/'))
    response = middleware(request)

    assert hasattr(request, 'session')
    assert getattr(request, '_using_custom_session', False) is True

@pytest.mark.django_db
def test_oauth_redirect_cookie_set(monkeypatch):
    monkeypatch.setattr(settings, "CHRONA_SESSION_COOKIE_NAME", "chrona-sessionid")
    monkeypatch.setattr(settings, "SESSION_COOKIE_AGE", 1209600)
    monkeypatch.setattr(settings, "SOCIAL_AUTH_LOGIN_REDIRECT_URL", "/auth-complete/")

    factory = RequestFactory()
    request = factory.get('/')
    request.session = SessionStore()
    request.session.create()  # ensures session_key exists
    request._using_custom_session = True

    view = lambda r: HttpResponseRedirect('/auth-complete/')
    middleware = SmartSessionMiddleware(view)
    response = middleware(request)

    assert response.status_code == 302
    assert response.url == '/auth-complete/'
    middleware = SmartSessionMiddleware(view)
    response = middleware(request)

    assert response.status_code == 302
    assert 'chrona-sessionid' in response.cookies
