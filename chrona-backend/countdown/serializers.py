from django.utils import timezone
from rest_framework import serializers

from .models import Timers


class TimerValidator:
    """
    Mixin class that provides validation logic for different timer endpoints:
    - /start/
    - /pause/
    - /completed/
    """

    def validate(self, attrs):
        """
        Route validation to the appropriate method based on the endpoint.
        """
        if self.context['endpoint'].endswith("pause/"):
            attrs = self.validate_pause(attrs)
        elif self.context['endpoint'].endswith('start/'):
            attrs = self.validate_start(attrs)
        elif self.context['endpoint'].endswith('completed/'):
            attrs = self.validate_completed(attrs)
        return super().validate(attrs)

    def validate_pause(self, attrs):
        """
        Update timer status to 'paused' and record the paused timestamp.
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
        Update or initialize timer for starting/resuming countdown.
        Sets resumed_at and resets pause.
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

    def validate_completed(self, attrs):
        """
        Mark timer as completed and reset relevant fields.
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
    Serializer for Timer model. Extends TimerValidator to handle
    logic specific to start, pause, and complete actions.
    """

    name = serializers.CharField(required=False)
    timestamp = serializers.DateTimeField(required=True, write_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Timers
        exclude = ['user_id']  # user_id is set automatically from request

    def create(self, validated_data):
        """
        Attach user from request and create timer.
        """
        validated_data['user_id'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Calculate remaining duration dynamically if timer is running.
        Automatically complete if time is up.
        """
        if not instance.paused_at and instance.resumed_at:
            elapsed = (timezone.now() - instance.resumed_at).total_seconds()
            remaining = instance.remaining_duration_seconds - elapsed

            if remaining <= 0:
                instance.status = 'completed'
                instance.remaining_duration_seconds = 0
                instance.save()
        return super().to_representation(instance)
