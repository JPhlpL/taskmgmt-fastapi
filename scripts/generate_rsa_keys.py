# generate_rsa_keys.py

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# 1) Generate private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

# 2) Serialize and save the private key (PKCS8/PEM)
pem_priv = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),  # or BestAvailableEncryption(b"passphrase")
)
with open("clerk_rsa_private.pem", "wb") as f:
    f.write(pem_priv)

# 3) Extract the public key
public_key = private_key.public_key()

# 4) Serialize and save the public key (SPKI/PEM)
pem_pub = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo,
)
with open("clerk_rsa_public.pem", "wb") as f:
    f.write(pem_pub)

print("✅ Generated clerk_rsa_private.pem and clerk_rsa_public.pem")
