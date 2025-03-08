from datetime import datetime


# function to calculate elapse time

def calculate_elapsed_time(start_time, pause_time=None):
    start = datetime.fromisoformat(start_time)
    pause = pause_time and datetime.fromisoformat(pause_time) or datetime.now()
    return (pause - start).total_seconds()