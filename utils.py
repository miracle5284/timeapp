from datetime import datetime, timedelta


def ensure_session(request):
    """Ensures a valid session exists."""
    print('session_node de')
    if not request.session.session_key:
        print('session de')
        request.session.create()


# function to calculate elapse time
def calculate_elapsed_time(start_time, pause_time=None):
    start = datetime.fromisoformat(start_time)
    pause = pause_time and datetime.fromisoformat(pause_time) or datetime.now()
    return (pause - start).total_seconds()


def calculate_end_time_in_string(start: str, duration: float | int) -> str:
    start = datetime.fromisoformat(start)
    return (start + timedelta(seconds=duration)).strftime('%Y-%m-%d %H:%M:%S')