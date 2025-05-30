import uuid

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from utils.fields import EncryptedCharField
from utils.orm import Model, models

User = get_user_model()

class Timers(Model):

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('expired', 'Expired'),
        ('completed', 'Completed'),
        ('inactive', 'Inactive')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timers')
    name = EncryptedCharField(max_length=255)
    duration_seconds = models.PositiveIntegerField(default=0)
    remaining_duration_seconds = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    is_recurring = models.BooleanField(default=False)
    start_at = models.DateTimeField(blank=True, null=True)
    paused_at = models.DateTimeField(blank=True, null=True)
    resumed_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = _('Timer'),
        verbose_name_plural = _('Timers')
        ordering = ['-updated_at']
        safe_search_fields = ['name']

    def __str__(self):
        return f"{self.name} ({self.user_id})"

    @property
    def is_active(self):
        return self.status == 'active'


class NotificationSettings(Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid5, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_settings')
    sound_enabled = models.BooleanField(default=True)
    browser_notifications_enabled = models.BooleanField(default=True)
    volume_level = models.PositiveIntegerField(default=50)
    vibrate_enabled = models.BooleanField(default=True)
    sound_file = models.FileField(upload_to='sounds/', blank=True, null=True)


