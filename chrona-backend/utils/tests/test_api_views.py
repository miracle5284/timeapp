from http.client import responses

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.conf import settings


@pytest.mark.django_db
def test_health_check_view():
    client = APIClient()
    url = reverse('health_check')
    response = client.get(url)

    assert response.status_code == 200
    assert response.data == {'status': 'ok'}

def test_extension_info(monkeypatch):
    from django.conf import settings
    monkeypatch.setattr(settings, "EXTENSION_ID", "abc123")
    monkeypatch.setattr(settings, "EXTENSION_NAME", "Chrona Extension")

    client = APIClient()
    url = reverse('extension-info')
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["EXTENSION_ID"] == "abc123"