import asyncio
import logging
import threading

from .redis_client import redis_client

class AsyncRedisStreamHandler(logging.Handler):

    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

        self.loop = asyncio.new_event_loop()
        self.redis_client = redis_client

        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def emit(self, record):
        print(f"Emitting log record to Redis: {record}")
        try:
            log_entry = self.format(record)
            future = asyncio.run_coroutine_threadsafe(
                self.redis_client.xadd("log_events", {
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
                "module": record.module,
                "user": getattr(record, 'user_id', 'unknown'),
                "full_message": log_entry,
            }), self.loop)
        except Exception:
            self.handleError(record)

    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()
        super().close()