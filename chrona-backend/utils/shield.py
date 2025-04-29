import hmac
import hashlib
from django.conf import settings


def compute_hmac(value: str, key: str=None) -> str:
    """
    Compute the HMAC of a given value using the provided key.

    :param value: The value to compute the HMAC for.
    :param key: The key to use for HMAC computation.
    :return: The computed HMAC as a hexadecimal string.
    """
    if not key:
        key = settings.HMAC_KEY
    return hmac.new(key.encode(), value.encode(), hashlib.sha256).hexdigest()

def verify_hmac(value: str, expected_hmac_value: str, key: str=None) -> bool:
    """
    Verify the HMAC of a given value using the provided key and HMAC value.

    :param value: The value to verify the HMAC for.
    :param key: The key to use for HMAC verification.
    :param expected_hmac_value: The HMAC value to verify against.
    :return: True if the HMAC is valid, False otherwise.
    """
    computed_hmac = compute_hmac(value, key)
    return hmac.compare_digest(computed_hmac, expected_hmac_value)