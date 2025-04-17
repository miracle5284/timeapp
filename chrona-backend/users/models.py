from django.db import models
from django.contrib.
from django.contrib.auth.models import AbstractUser
from utils.orm import SmartUserManager, Model as SmartModel
from django.utils.translation import gettext_lazy as _
from utils.fields import EncryptedEmailField, EncryptedCharField


class User(AbstractUser, SmartModel):
    """
    Custom User model that uses email as the unique identifier.
    """

    email = EncryptedEmailField(unique=True)
    first_name = EncryptedCharField(max_length=30, blank=True)
    last_name = EncryptedCharField(max_length=30, blank=True)
    username = EncryptedCharField(max_length=150, unique=True)

    account_id = EncryptedCharField(max_length=25, unique=True)


    objects = SmartUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        safe_search_fields = ['email', 'username', 'first_name', 'last_name']
