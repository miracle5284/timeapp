from django.db import models
from .shield import compute_hmac
from .fields import EncryptedTextField
from django.contrib.auth.models import UserManager


class HMACModelBase(models.base.ModelBase):
    """
    Metaclass that auto-generates HMAC shadow fields for models using encrypted fields
    marked as `safe_search_fields` in their Meta class.

    This enables deterministic, secure lookups on encrypted data fields.
    """
    def __new__(cls, name, bases, attrs, **kwargs):
        meta = attrs.get('Meta', None)
        safe_search = getattr(meta, 'safe_search_fields', [])

        for field_name in safe_search:
            # Try to locate the encrypted field being referenced
            original_field = attrs.get(field_name) or next(
                (f for f in [base._meta.get_field(field_name) for base in bases
                 if hasattr(base, '_meta') and base._meta.apps.ready]
                 if getattr(f, '_encryption', None)),
                None
            )
            if not original_field:
                raise TypeError(f"Field '{field_name}' must exist and be an EncryptedField to be safe_searchable.")

            hmac_field_name = f"_{field_name}_hmac"
            if hmac_field_name not in attrs:
                field_class = type(original_field)
                max_length = getattr(original_field, 'max_length', 255)

                # TODO - check if the field is a TextField or CharField
                # if isinstance(original_field, EncryptedTextField):
                #     attrs[hmac_field_name] = models.TextField(editable=False, db_index=True)
                # else:

                # Default: create CharField as HMAC mirror field
                attrs[hmac_field_name] = models.CharField(editable=False, db_index=True)

        return super().__new__(cls, name, bases, attrs, **kwargs)


class SmartQueryset(models.QuerySet):
    """
    Custom QuerySet that handles transparent HMAC substitution for filters on encrypted fields,
    and decrypts data when calling `.values()` or `.values_list()`.
    """

    def _resolve_filter_args(self, kwargs):
        """
        Translates user filters on encrypted fields into HMAC field lookups.
        """
        resolved_kwargs = {}
        search_fields = getattr(self.model._meta, 'safe_search_fields', [])

        for key, value in kwargs.items():
            if key in search_fields:
                resolved_kwargs[f"_{key}_hmac"] = compute_hmac(value)
            else:
                resolved_kwargs[key] = value

        return resolved_kwargs

    def get(self, *args, **kwargs):
        """Overrides get() to support filtering with encrypted field HMACs."""
        return super().get(*args, **self._resolve_filter_args(kwargs))

    def filter(self, *args, **kwargs):
        """Overrides filter() to support HMAC-based lookup on encrypted fields."""
        return super().filter(*args, **self._resolve_filter_args(kwargs))

    def values(self, *fields, **expressions):
        """
        Overrides values() to decrypt encrypted field values and omit HMAC fields
        from the returned dictionaries.
        """
        raw = super().values(*fields, **expressions)

        def decrypt_rows():
            for row in raw:
                clean = {}
                for field_name, value in row.items():
                    if field_name.endswith('_hmac'):
                        continue  # Skip internal HMAC fields
                    model_field = self.model._meta.get_field(field_name)
                    if getattr(model_field, '_encryption', None) and value is not None:
                        try:
                            clean[field_name] = model_field.from_db_value(value, None, None)
                        except Exception:
                            clean[field_name] = value
                    else:
                        clean[field_name] = value
                yield clean

        return decrypt_rows()

    def values_list(self, *fields, **kwargs):
        """
        Overrides values_list() to decrypt encrypted values and omit HMACs,
        yielding result rows as tuples.
        """
        raw = super().values(*fields, **kwargs)

        def decrypt_rows():
            for row in raw:
                clean = []
                for field_name, value in row.items():
                    if field_name.endswith('_hmac'):
                        continue  # Skip internal HMAC fields
                    model_field = self.model._meta.get_field(field_name)
                    if getattr(model_field, '_encryption', None) and value is not None:
                        try:
                            clean.append(model_field.from_db_value(value, None, None))
                        except Exception:
                            clean.append(value)
                    else:
                        clean.append(value)
                yield tuple(clean)

        return decrypt_rows()


class SmartManager(models.Manager):
    """
    Manager that uses SmartQueryset with HMAC lookup and encrypted field support.
    """
    def get_queryset(self):
        return SmartQueryset(self.model, using=self._db)


class SmartUserManager(SmartManager, UserManager):
    """
    Combined manager for Django user models with HMAC lookup support.
    """
    pass


class Model(models.Model, metaclass=HMACModelBase):
    """
    Abstract base model class that:
    - Automatically manages HMAC field values on save
    - Enables secure filtering and querying of encrypted fields using SmartQueryset
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Computes and stores HMAC values for all safe_search_fields before saving.
        """
        safe_search_fields = getattr(self._meta, 'safe_search_fields', [])
        for fields in safe_search_fields:
            val = getattr(self, fields, None)
            if val:
                setattr(self, f"_{fields}_hmac", compute_hmac(val))
        return super().save(*args, **kwargs)

    objects = SmartManager()
