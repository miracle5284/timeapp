from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.orm import SmartUserManager, Model as SmartModel
from django.utils.translation import gettext_lazy as _
from utils.fields import EncryptedEmailField, EncryptedCharField


class User(SmartModel, AbstractUser):
    """
    Custom User model that uses email as the unique identifier.
    """

    email = EncryptedEmailField(unique=True, null=False, default=None)
    first_name = EncryptedCharField(max_length=30, blank=True)
    last_name = EncryptedCharField(max_length=30, blank=True)
    username = EncryptedCharField(max_length=150, unique=True, null=False, default=None)

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

#
# class UserProfile(models.Model):
#     """
#     User profile model to store additional information about the user.
#     """
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username}'s Profile"