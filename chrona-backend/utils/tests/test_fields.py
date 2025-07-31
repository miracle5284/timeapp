import pytest
from django.db import models
from utils.fields import EncryptedCharField
from django.conf import settings
from cryptography.fernet import Fernet


class TestModel(models.Model):
    name = EncryptedCharField(max_length=225, null=True)

    class Meta:
        app_label = "utils"

@pytest.mark.django_db
def test_encrypted_char_field_behavior():
    secret = 'TopSecretData'
    cipher = Fernet(settings.FERNET_ENCRYPTION_KEY)
    field = EncryptedCharField()

    encrypted = field.get_prep_value(secret)
    assert encrypted != secret
    assert cipher.decrypt(encrypted.encode()).decode() == secret

    decrypted = field.from_db_value(encrypted, None, None)
    assert decrypted == secret

