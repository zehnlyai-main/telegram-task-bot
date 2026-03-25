import os
from cryptography.fernet import Fernet

_key = os.getenv("ENCRYPTION_KEY")
if not _key:
    generated = Fernet.generate_key().decode()
    print(f"\n⚠️  ENCRYPTION_KEY not set. Add this to your .env file:\nENCRYPTION_KEY={generated}\n")
    _key = generated

_fernet = Fernet(_key.encode() if isinstance(_key, str) else _key)


def encrypt(plaintext: str) -> str:
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    return _fernet.decrypt(ciphertext.encode()).decode()
