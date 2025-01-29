from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import json

# Create your views here.
def home(request):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    duration = request.session.get('duration', 0)
    initial_duration = request.session.get('initial_duration', 0)
    pause_time = request.session.get('pause_time')
    start_time = request.session.get('start_time')
    time_up = False
    if duration > 0:

        print(1111, start_time, pause_time)
        if start_time:

            if not pause_time:
                duration -= (datetime.now() - datetime.fromisoformat(start_time)).total_seconds()

            else:
                duration -= (datetime.fromisoformat(pause_time) - datetime.fromisoformat(start_time)).total_seconds()
            print(111, duration)
            if duration <= 0:
                duration = 0
                time_up = True

    hour, remaining_duration = divmod(duration, 3600)
    minutes, seconds = divmod(remaining_duration, 60)
    print(333, time_up, initial_duration)

    return render(request, 'timer.html', {"time_maps": {'Hours': int(hour), 'Minutes': int(minutes), 'Seconds': int(seconds)}
                                          , 'time_up': time_up, 'initial_duration': initial_duration,
                  "active": bool(pause_time is None and start_time and duration)})

@require_http_methods(['POST'])
def set_timer(request):
    session_key = request.session.session_key
    print(111, request.POST, request.body)
    data = json.loads(request.body)
    duration = int(data['duration'])
    initial_duration = int(data['initialDuration'])
    request.session['duration'] = duration
    request.session['initial_duration'] = initial_duration
    request.session['start_time'] = datetime.now().isoformat()
    request.session['pause_time'] = None

    return JsonResponse({'success': True})

@require_http_methods(['PUT'])
def pause_timer(request):
    # session_key = request.session.session_key
    data = json.loads(request.body)
    # duration = int(data['duration'])
    # request.session['duration'] = duration
    request.session['pause_time'] = datetime.now().isoformat()

    return JsonResponse({'success': True})

@require_http_methods(['PUT'])
def reset_timer(request):
    request.session['duration'] = request.session.get('initial_duration', 0)
    request.session['start_time'] = None
    request.session['pause_time'] = None

    return JsonResponse({'success': True})
