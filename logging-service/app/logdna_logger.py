import logging
import time

import requests

from . import config
from logdna import LogDNAHandler

class PersistentLogDNAHandler(LogDNAHandler):

    def __init__(self, key, options=None):

        self.options = options or {}
        super().__init__(key, self.options)

        self.session = requests.Session()
        self.session.headers.update({
            # 'Content-Type': 'application/json',
            # "Accept": "application/json",
            'user-agent': self.user_agent,
            'apikey': self.key
        })

    def send_request(self, data):
        return _send_request(self, data)


# Get your LogDNA Ingestion Key from the environment (or set a default for development)
# Additional options for LogDNA (customize as needed)
LOGDNA_OPTIONS = {
    "hostname": "logging-service",
    "index_meta": True,
}

# Create a dedicated logger for shipping logs to LogDNA
logger = logging.getLogger("logdna_logger")
# logger.setLevel(logging.INFO)

# Avoid adding duplicate handlers if this module is imported multiple times
if not logger.handlers:
    handler = PersistentLogDNAHandler(key=config.LOGDNA_INGESTION_KEY, options=LOGDNA_OPTIONS)
    handler.setLevel(logging.INFO)
    # Set a simple JSON or standard formatter.
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s: %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def send_log_to_logdna(message, level=logging.INFO, extra=None):
    """
    Send a log message to LogDNA using the preconfigured logger.

    :param message: The log message to send.
    :param level: Logging level (e.g., logging.INFO, logging.ERROR).
    :param extra: Optional dict of additional context.
    """
    logger.setLevel(level)
    print('SSSSSSS: ', level)
    logger.log(level, message, extra=extra)




def _send_request(self, data):  # noqa: max-complexity: 13
    """
        Send log data to LogDNA server
    Returns:
        True  - discard flush buffer
        False - retry, keep flush buffer
    """
    try:
        response = self.session.post(url=self.url,
                                 json=data,
                                 params={
                                     'hostname': self.hostname,
                                     'ip': self.ip,
                                     'mac': self.mac,
                                     'tags': self.tags,
                                     'now': int(time.time() * 1000)
                                 },
                                 stream=True,
                                 allow_redirects=True,
                                 timeout=self.request_timeout)

        status_code = response.status_code
        '''
            response code:
                1XX                       unexpected status
                200                       expected status, OK
                2XX                       unexpected status
                301 302 303               unexpected status,
                                          per "allow_redirects=True"
                3XX                       unexpected status
                401, 403                  expected client error,
                                          invalid ingestion key
                429                       expected server error,
                                          "client error", transient
                4XX                       unexpected client error
                500 502 503 504 507       expected server error, transient
                5XX                       unexpected server error
            handling:
                expected status           discard flush buffer
                unexpected status         log + discard flush buffer
                expected client error     log + discard flush buffer
                unexpected client error   log + discard flush buffer
                expected server error     log + retry
                unexpected server error   log + discard flush buffer
        '''
        if status_code == 200:
            return True  # discard

        if isinstance(response.reason, bytes):
            # We attempt to decode utf-8 first because some servers
            # choose to localize their reason strings. If the string
            # isn't utf-8, we fall back to iso-8859-1 for all other
            # encodings. (See PR #3538)
            try:
                reason = response.reason.decode('utf-8')
            except UnicodeDecodeError:
                reason = response.reason.decode('iso-8859-1')
        else:
            reason = response.reason

        if 200 < status_code <= 399:
            self.internalLogger.debug('Unexpected response: %s. ' +
                                      'Discarding flush buffer',
                                      reason)
            if self.log_error_response:
                self.internalLogger.debug(
                    'Error Response: %s', response.text)
            return True  # discard

        if status_code in [401, 403]:
            self.internalLogger.debug(
                'Please provide a valid ingestion key. ' +
                'Discarding flush buffer')
            if self.log_error_response:
                self.internalLogger.debug(
                    'Error Response: %s', response.text)
            return True  # discard

        if status_code == 429:
            self.internalLogger.debug('Client Error: %s. Retrying...',
                                      reason)
            if self.log_error_response:
                self.internalLogger.debug(
                    'Error Response: %s', response.text)
            return False  # retry

        if 400 <= status_code <= 499:
            self.internalLogger.debug('Client Error: %s. ' +
                                      'Discarding flush buffer',
                                      reason)
            if self.log_error_response:
                self.internalLogger.debug(
                    'Error Response: %s', response.text)
            return True  # discard

        if status_code in [500, 502, 503, 504, 507]:
            self.internalLogger.debug('Server Error: %s. Retrying...',
                                      reason)
            if self.log_error_response:
                self.internalLogger.debug(
                    'Error Response: %s', response.text)
            return False  # retry

        self.internalLogger.debug('The request failed: %s.' +
                                  'Discarding flush buffer',
                                  reason)

    except requests.exceptions.Timeout as timeout:
        self.internalLogger.debug('Timeout Error: %s. Retrying...',
                                  timeout)
        return False  # retry

    except requests.exceptions.RequestException as exception:
        self.internalLogger.debug(
            'Error sending logs %s. Discarding flush buffer', exception)

    return True  # discard