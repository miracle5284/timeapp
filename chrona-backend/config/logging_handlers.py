import asyncio
import logging
import threading

from .redis_client import redis_client


class AsyncRedisStreamHandler(logging.Handler):
    """
    A custom asynchronous logging handler that sends log records to a Redis Stream.

    This handler integrates asyncio and threading to asynchronously publish
    logging records to Redis without blocking the main application.
    """

    def __init__(self, level=logging.NOTSET):
        """
        Initializes the AsyncRedisStreamHandler.

        Args:
            level (int): The log level threshold.
        """
        super().__init__(level)

        # Create a new asyncio event loop for handling Redis operations asynchronously
        self.loop = asyncio.new_event_loop()
        self.redis_client = redis_client

        # Start the event loop in a separate daemon thread to handle async tasks
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        """
        Runs the asyncio event loop indefinitely in a separate thread.
        """
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def emit(self, record):
        """
        Formats and asynchronously emits a logging record to the Redis Stream.

        Args:
            record (logging.LogRecord): The logging record to emit.
        """
        # Debug print statement for visibility during development
        print(f"Emitting log record to Redis: {record}")

        try:
            # Format the log entry into a structured string
            log_entry = self.format(record)

            # Schedule the coroutine safely in the running event loop
            future = asyncio.run_coroutine_threadsafe(
                self.redis_client.xadd("log_events", {
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "logger": record.name,
                    "module": record.module,
                    "user": getattr(record, 'user_id', 'unknown'),  # user ID if available
                    "full_message": log_entry,
                }), self.loop
            )

            # Optionally handle the result or exceptions here

        except Exception:
            # Handle exceptions during logging to prevent disruption of main app
            self.handleError(record)

    def close(self):
        """
        Cleanly shuts down the asyncio loop and the associated thread.
        """
        # Signal the loop to stop and wait for the thread to finish
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

        # Properly close the logging handler
        super().close()
