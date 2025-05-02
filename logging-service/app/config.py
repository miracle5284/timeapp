# app/config.py
from decouple import config

REDIS_HOST = config("REDIS-HOST".lower(), default="localhost")
REDIS_PORT = config("REDIS-PORT".lower(), default="6379")
REDIS_PASSWORD = config("REDIS-PASSWORD".lower())
LOG_STREAM = config("LOG-STREAM".lower(), default="log_events")
LOGDNA_API_KEY = config("LOGDNA-API-KEY".lower(), default=None)
SENTRY_DSN = config("SENTRY-DSN".lower(), default=None)
PROMETHEUS_PUSHGATEWAY_URL = config("PROMETHEUS-PUSHGATEWAY-URL".lower(), default="http://pushgateway:9091")
LOGDNA_INGESTION_KEY = config("LOGDNA-INGESTION-KEY".lower(), default=None)
