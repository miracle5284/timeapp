from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate key pair
private_key = ec.generate_private_key(ec.SECP256R1())
public_key = private_key.public_key()

# Export public key (Base64 URL-safe)
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)
public_key_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')

# Export private key
private_bytes = private_key.private_numbers().private_value.to_bytes(32, 'big')
private_key_b64 = base64.urlsafe_b64encode(private_bytes).decode('utf-8').rstrip('=')

print("VAPID_PUBLIC_KEY =", public_key_b64)
print("VAPID_PRIVATE_KEY =", private_key_b64)
