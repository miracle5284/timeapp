from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .utils import calculate_elapsed_time
import json
import logging
import random

# Initialize logger for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_session(request):
    """Ensures a valid session exists."""
    if not request.session.session_key:
        request.session.create()

# Home View: Renders the timer with stored session data

STYLES = ['animate-styling.css', 'style.css', 'style-cool.css', 'style-white.css']
def home(request):
    ensure_session(request)

    try:
        duration = request.session.get('duration', 0)
        initial_duration = request.session.get('initial_duration', 0)
        pause_time = request.session.get('pause_time')
        start_time = request.session.get('start_time')
        time_up = False

        # Check if a style is already stored in session
        style = request.session.get('selected_style')

        if not style or calculate_elapsed_time(style.get('start_time')) > 3600:
            # If not, select a random style and store it in session
            request.session['selected_style'] = style = {
                'style': random.choice(STYLES),
                'start_time': datetime.now().isoformat()
            }

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

        hour, remaining_duration = divmod(max(0, duration), 3600)
        minutes, seconds = divmod(remaining_duration, 60)

        return render(request, 'timer.html', {
            "time_maps": {'Hours': int(hour), 'Minutes': int(minutes), 'Seconds': int(seconds)},
            'time_up': time_up,
            'initial_duration': initial_duration,
            "active": bool(not pause_time and start_time and duration),
            'style': style.get('style')
        })

    except Exception as e:
        logger.error(f"Error in home view: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

# API: Set Timer
@require_http_methods(['POST'])
def set_timer(request):
    ensure_session(request)

    try:
        data = json.loads(request.body)

        # Validate input keys
        if 'duration' not in data or 'initialDuration' not in data:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Validate duration values
        duration = int(data['duration'])
        initial_duration = int(data['initialDuration'])

        if duration <= 0 or initial_duration <= 0:
            return JsonResponse({'error': 'Duration must be greater than zero'}, status=400)

        request.session['duration'] = duration
        request.session['initial_duration'] = initial_duration
        request.session['start_time'] = datetime.now().isoformat()
        request.session['pause_time'] = None

        return JsonResponse({'success': True})

    except (json.JSONDecodeError, ValueError) as e:
        logger.error(f"Invalid request data in set_timer: {e}")
        return JsonResponse({'error': 'Invalid input data'}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error in set_timer: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

# API: Pause Timer
@require_http_methods(['PUT'])
def pause_timer(request):
    ensure_session(request)

    try:
        start_time = request.session.get('start_time')
        duration = request.session.get('duration', 0)

        # Prevent pausing if no active timer
        if not start_time or duration <= 0:
            return JsonResponse({'error': 'No active timer to pause'}, status=400)

        request.session['pause_time'] = datetime.now().isoformat()
        return JsonResponse({'success': True})

    except Exception as e:
        logger.error(f"Error in pause_timer: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

# API: Reset Timer
@require_http_methods(['PUT'])
def reset_timer(request):
    ensure_session(request)

    try:
        initial_duration = request.session.get('initial_duration', 0)

        # Reset only if an initial duration exists
        if initial_duration <= 0:
            return JsonResponse({'error': 'No timer has been set'}, status=428)

        request.session['duration'] = initial_duration
        request.session['start_time'] = None
        request.session['pause_time'] = None

        return JsonResponse({'success': True})

    except Exception as e:
        logger.error(f"Error in reset_timer: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)
