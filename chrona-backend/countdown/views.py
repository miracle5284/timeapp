import logging
from rest_framework.response import Response
from rest_framework.decorators import action

from countdown.serializers import TimerSerializer, Timers
from utils.views import BaseModelViewSet

# Initialize logger for debugging and observability
logger = logging.getLogger(__name__)


class TimerViewSet(BaseModelViewSet):
    """
    A ViewSet for managing Timer instances.
    Supports starting, pausing, resetting, and completing timers via custom PATCH endpoints.
    """

    serializer_class = TimerSerializer

    @action(methods=['patch'], detail=True)
    def pause(self, request, **kwargs):
        """
        PATCH endpoint to pause a timer.
        Delegates to the base update method after setting context for validation.
        """
        return super().update(request, partial=True, **kwargs)

    @action(methods=['patch'], detail=True)
    def start(self, request, **kwargs):
        """
        PATCH endpoint to start or resume a timer.
        Delegates to the base update method after setting context for validation.
        """
        return super().update(request, partial=True, **kwargs)

    @action(methods=['patch'], detail=True)
    def reset(self, request, **kwargs):
        """
        PATCH endpoint to reset a timer.
        Delegates to the base update method after setting context for validation.
        """
        return super().update(request, partial=True, **kwargs)

    @action(methods=['patch'], detail=True)
    def completed(self, request, **kwargs):
        """
        PATCH endpoint to mark a timer as completed.
        Delegates to the base update method after setting context for validation.
        """
        return super().update(request, partial=True, **kwargs)

    def get_serializer_context(self):
        """
        Extend serializer context to include the current request path.
        This allows the serializer to determine which validation logic to apply.
        """
        context = super().get_serializer_context()
        context['endpoint'] = self.request.path
        return context

    @action(methods=['patch'], detail=True)
    def rename(self, request, **kwargs):
        data = self.partial_update(request, **kwargs)
        return Response({"data": {"name": data.data['name']}, "message": "Timer renamed successfully."}, status=200)

