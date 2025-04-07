from datetime import datetime

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils import ensure_session, calculate_elapsed_time, calculate_end_time_in_string

import logging
import random
import json


# Initialize logger for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CountDownView(APIView):
    """
    Countdown API view to handle countdown timer operations.
    """



    def get(self, request):
        ensure_session(request)

        try:
            duration = request.session.get('duration', 0)
            set_duration = request.session.get('set_duration', 0)
            pause_time = request.session.get('pause_time')
            start_time = request.session.get('start_time')
            time_up = False

            print(111, duration, set_duration, start_time)

            if duration > 0 and start_time:
                try:
                    duration -= calculate_elapsed_time(start_time, pause_time)

                    if duration <= 0:
                        duration = 0
                        time_up = True

                except ValueError:
                    logger.error("Invalid datetime format in session. Resetting timer.")
                    request.session['start_time'] = None
                    request.session['pause_time'] = None
                    duration = 0
            active = bool(not pause_time and start_time and duration)
            return Response({
                'duration': duration,
                'timeUp': time_up,
                'setDuration': set_duration,
                "active": active,
                "endTime": (active and calculate_end_time_in_string(start_time, duration) or None),
                'extensionId': settings.EXTENSION_ID
            })

        except Exception as e:
            logger.error(f"Error in home view: {e}")
            return Response({'error': 'Internal server error'}, status=500)

    def post(self, request):
        """
        Start or reset the countdown timer.
        """
        ensure_session(request)

        try:
            data = json.loads(request.body)

            # Validate input keys
            if 'duration' not in data or 'setDuration' not in data:
                return Response({'error': 'Missing required field, duration'}, status=400)

            # Validate duration values
            duration = int(data['duration'])
            set_duration = int(data['setDuration'])

            if duration <= 0:# or set_duration <= 0:
                return Response({'error': 'Duration must be greater than zero'}, status=400)

            request.session['duration'] = duration
            request.session['set_duration'] = set_duration
            request.session['start_time'] = datetime.now().isoformat()
            request.session['pause_time'] = None

            return Response({'success': True})

        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Invalid request data in set_timer: {e}")
            return Response({'error': 'Invalid input data'}, status=400)

        except Exception as e:
            logger.error(f"Unexpected error in set_timer: {e}")
            return Response({'error': 'Internal server error'}, status=500)

    def put(self, request):
        """
        Pause the countdown timer.
        """
        ensure_session(request)

        try:
            start_time = request.session.get('start_time')
            duration = request.session.get('duration', 0)

            # Prevent pausing if no active timer
            if not start_time or duration <= 0:
                return Response({'error': 'No active timer to pause'}, status=400)

            request.session['pause_time'] = datetime.now().isoformat()
            return Response({'success': True})

        except Exception as e:
            logger.error(f"Unexpected error in pause_timer: {e}")
            return Response({'error': 'Internal server error'}, status=500)

    def delete(self, request):
        ensure_session(request)

        try:
            set_duration = request.session.get('set_duration', 0)

            # Reset only if an initial duration exists
            if set_duration <= 0:
                return Response({'error': 'No timer has been set'}, status=428)

            request.session['duration'] = set_duration
            request.session['start_time'] = None
            request.session['pause_time'] = None

            return Response({'success': True})

        except ImportError as e:
            logger.error(f"Error in reset_timer: {e}")
            return Response({'error': 'Internal server error'}, status=500)