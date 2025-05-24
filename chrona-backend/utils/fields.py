from django.db import models
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from utils.shield import compute_hmac


class EncryptedFieldMixin:
    """
    Mixin to add transparent encryption/decryption behavior to Django model fields.
    Utilizes Fernet symmetric encryption with AES-128 in CBC mode.

    Any model field subclassing this mixin will:
    - Encrypt values before saving to the database
    - Decrypt values when fetched from the database
    - Mark itself as encrypted via `_encryption = True` attribute
    """

    _encryption = True  # Used to identify fields that need encryption

    @staticmethod
    def get_cipher():
        """
        Returns a Fernet cipher initialized with a shared secret key.
        Assumes the key is defined in Django settings as FERNET_ENCRYPTION_KEY.
        """
        return Fernet(settings.FERNET_ENCRYPTION_KEY)

    def get_prep_value(self, value):
        """
        Encrypts the value before saving to the DB.
        """
        if value is None:
            return None
        return self.get_cipher().encrypt(value.encode()).decode()

    def from_db_value(self, value, expression, connection):
        """
        Decrypts the value after reading from the DB.
        Handles legacy unencrypted values gracefully.
        """
        if value is None:
            return None
        try:
            return self.get_cipher().decrypt(value.encode()).decode()
        except InvalidToken:
            # Possibly legacy (plaintext) data or invalid encryption
            return value

    @staticmethod
    def get_internal_type():
        """
        Ensures that Django migration system treats this as a TextField.
        """
        return "TextField"

    def deconstruct(self):
        """
        Cleanly deconstruct field for migration generation.
        Removes `max_length` to avoid issues with Fernet-encrypted values.
        """
        name, path, args, kwargs = super().deconstruct()
        if 'max_length' in kwargs:
            del kwargs['max_length']
        # Ensure null, blank, unique, etc. are included in migration
        kwargs['null'] = self.null
        kwargs['blank'] = self.blank
        kwargs['unique'] = self.unique

        return name, path, args, kwargs


class HMACFieldMixin(models.CharField):
    """
    A CharField that stores a deterministic HMAC of a sensitive value for secure indexed lookups.
    Should be used as a shadow field to enable encrypted field search.
    """

    def __init__(self, source_fields=None, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 64  # Size of HMAC output in hex
        self.source_fields = source_fields  # The encrypted field this HMAC tracks
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Automatically computes HMAC from the linked field’s value on save.
        """
        if self.source_fields:
            value = getattr(model_instance, self.source_fields)
            if value:
                hmac_value = compute_hmac(value)
                setattr(model_instance, self.attname, hmac_value)
                return hmac_value
        return super().pre_save(model_instance, add)


# Concrete encrypted field implementations

class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    """
    CharField that encrypts/decrypts its value transparently.
    """
    pass


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    """
    TextField that encrypts/decrypts its value transparently.
    """
    pass


class EncryptedEmailField(EncryptedFieldMixin, models.EmailField):
    """
    EmailField that encrypts/decrypts its value transparently.
    """
    pass
