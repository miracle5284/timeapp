import logging
from .redis_client import redis_client

class RedisStreamHandler(logging.Handler):
    def emit(self, record):
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
