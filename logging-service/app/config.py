# app/config.py
from decouple import config

REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", default="6379")
LOG_STREAM = config("LOG_STREAM", default="log_events")
LOGDNA_API_KEY = config("LOGDNA_API_KEY", default=None)
SENTRY_DSN = config("SENTRY_DSN", default=None)
PROMETHEUS_PUSHGATEWAY_URL = config("PROMETHEUS_PUSHGATEWAY_URL", default="http://pushgateway:9091")
LOGDNA_INGESTION_KEY = config("LOGDNA_INGESTION_KEY", default=None)
