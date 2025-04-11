import logging
from .redis_client import redis_client

class RedisStreamHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.redis_client = redis_client

    def emit(self, record):
        print(f"Emitting log record to Redis: {record}")
        try:
            log_entry = self.format(record)
            redis_client.xadd("log_events", {
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
                "module": record.module,
                "user": getattr(record, 'user_id', 'unknown'),
                "full_message": log_entry,
            })
        except Exception:
            self.handleError(record)
