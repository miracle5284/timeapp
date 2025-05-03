from django.utils import timezone
from rest_framework import serializers

from .models import Timers


class TimerValidator:
    """
    Mixin class providing validation logic for different timer actions:
    - /start/ → Start or resume a timer
    - /pause/ → Pause a running timer
    - /completed/ → Mark a timer as completed
    - /reset/ → Reset a timer to initial inactive state
    """

    def validate(self, attrs):
        """
        Dispatch validation based on the current endpoint path.

        Args:
            attrs (dict): Incoming validated attributes.

        Returns:
            dict: Updated validated attributes.
        """
        if self.context['endpoint'].endswith("pause/"):
            attrs = self.validate_pause(attrs)
        elif self.context['endpoint'].endswith('start/'):
            attrs = self.validate_start(attrs)
        elif self.context['endpoint'].endswith('completed/'):
            attrs = self.validate_completed(attrs)
        elif self.context['endpoint'].endswith('reset/'):
            attrs = self.validate_reset(attrs)
        return super().validate(attrs)

    def validate_pause(self, attrs):
        """
        Handle pausing the timer: record paused time and set status to 'paused'.
        """
        timestamp = attrs.pop('timestamp')
        attrs.update({
            'status': 'paused',
            'paused_at': timestamp,
            'resumed_at': None
        })
        return attrs

    def validate_start(self, attrs):
        """
        Handle starting or resuming the timer:
        - If new, set `start_at`.
        - If restarting with different duration, update remaining duration.
        - Set `resumed_at` and clear any pause.
        """
        timestamp = attrs.pop('timestamp')

        # If it's a new instance, set start time
        if not self.instance or not self.instance.start_at:
            attrs['start_at'] = timestamp

        # Reset remaining duration if timer is being restarted with a new duration
        if self.instance and (
            self.instance.duration_seconds != attrs.get('duration_seconds') or
            not self.instance.remaining_duration_seconds
        ):
            attrs['remaining_duration_seconds'] = attrs.get('duration_seconds')

        attrs.update({
            'status': 'active',
            'paused_at': None,
            'resumed_at': timestamp
        })
        return attrs

    def validate_reset(self, attrs):
        """
        Handle resetting the timer back to its initial state:
        - Clears pause/resume timestamps.
        - Resets status to 'inactive'.
        - Resets remaining duration to the full duration.
        """
        attrs.update({
            'paused_at': None,
            'resumed_at': None,
            'status': 'inactive',
            'remaining_duration_seconds': self.instance.duration_seconds,
        })
        return attrs

    def validate_completed(self, attrs):
        """
        Handle marking the timer as completed:
        - Set paused_at to now.
        - Set status to 'completed'.
        - Zero out remaining duration.
        """
        timestamp = attrs.pop('timestamp')
        attrs.update({
            'paused_at': timestamp,
            'resumed_at': None,
            'status': 'completed',
            'remaining_duration_seconds': 0,
        })
        return attrs


class TimerSerializer(TimerValidator, serializers.ModelSerializer):
    """
    Serializer for the Timer model, with validation extensions
    for handling specific timer lifecycle events (start, pause, reset, complete).
    """

    name = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=True, write_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Timers
        exclude = ['user_id'] #, 'celery_tracking_id']  # user_id will be set during create from the request context

    def create(self, validated_data):
        """
        Create a new timer instance, automatically attaching the authenticated user.

        Args:
            validated_data (dict): Incoming validated data.

        Returns:
            Timers: Newly created timer instance.
        """
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Dynamically adjust the representation of the timer:
        - If the timer is active and not paused, calculate updated remaining time.
        - If time is exhausted, mark the timer as 'completed' automatically.

        Args:
            instance (Timers): Timer model instance.

        Returns:
            dict: Serialized timer data for API response.
        """
        if not instance.paused_at and instance.resumed_at:
            elapsed = (timezone.now() - instance.resumed_at).total_seconds()
            instance.remaining_duration_seconds = max(0, instance.remaining_duration_seconds - elapsed)

            if instance.remaining_duration_seconds == 0:
                instance.status = 'completed'
                instance.save()

        return super().to_representation(instance)
