import os
from decouple import config

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STREAM_KEY = os.getenv("REDIS_STREAM_KEY", "log_events")

SENTRY_DSN = os.getenv("SENTRY_DSN")
LOGDNA_INGEST_KEY = os.getenv("LOGDNA_INGEST_KEY")
PUSHGATEWAY_URL = os.getenv("PUSHGATEWAY_URL", "http://localhost:9091")
