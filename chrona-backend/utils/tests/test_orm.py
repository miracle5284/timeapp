import pytest
from django.db import models, connection

from utils.orm import Model, SmartManager
from utils.fields import EncryptedCharField
from django.conf import settings
from utils.shield import compute_hmac
from cryptography.fernet import Fernet


@pytest.fixture(scope='module')
def dynamic_secure_model(django_db_setup, django_db_blocker):
    # Concrete model for testing
    class MockSecureModel(Model):
        name = EncryptedCharField(max_length=255)
        _name_hmac = models.CharField(max_length=255, db_index=True)

        objects = SmartManager()

        class Meta:
            app_label = "utils"
            safe_search_fields = ["name"]

    with django_db_blocker.unblock():
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(MockSecureModel)
        yield MockSecureModel
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(MockSecureModel)



@pytest.mark.django_db
def test_save_generates_hmac(monkeypatch, dynamic_secure_model):
    monkeypatch.setattr(settings, "FERNET_ENCRYPTION_KEY", Fernet.generate_key())
    obj = dynamic_secure_model(name="secret")
    obj.save()

    assert obj._name_hmac == compute_hmac("secret")
    assert dynamic_secure_model.objects.filter(name="secret").exists()


@pytest.mark.django_db
def test_values_omits_hmac(monkeypatch, dynamic_secure_model):
    monkeypatch.setattr(settings, "FERNET_ENCRYPTION_KEY", Fernet.generate_key())
    obj = dynamic_secure_model.objects.create(name="agentx")
    rows = list(dynamic_secure_model.objects.values())
    assert all("_name_hmac" not in row for row in rows)
    assert rows[0]["name"] == "agentx"
