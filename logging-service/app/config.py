# app/config.py
from decouple import config

REDIS_HOST = config("REDIS-HOST", default="localhost")
REDIS_PORT = config("REDIS-PORT", default="6379")
REDIS_PASSWORD = config("REDIS-PASSWORD")
LOG_STREAM = config("LOG-STREAM", default="log_events")
LOGDNA_API_KEY = config("LOGDNA-API-KEY", default=None)
SENTRY_DSN = config("SENTRY-DSN", default=None)
PROMETHEUS_PUSHGATEWAY_URL = config("PROMETHEUS-PUSHGATEWAY-URL", default="http://pushgateway:9091")
LOGDNA_INGESTION_KEY = config("LOGDNA-INGESTION-KEY", default=None)
