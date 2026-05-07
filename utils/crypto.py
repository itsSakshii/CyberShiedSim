import base64
import hashlib

from cryptography.fernet import Fernet


def generate_fernet_key() -> bytes:
    return Fernet.generate_key()


def encrypt_text_fernet(text: str, key: bytes) -> str:
    token = Fernet(key).encrypt(text.encode())
    return token.decode()


def decrypt_text_fernet(token: str, key: bytes) -> str:
    plain = Fernet(key).decrypt(token.encode())
    return plain.decode(errors="ignore")


def encrypt_bytes_fernet(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt_bytes_fernet(data: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(data)


def sha256_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def md5_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def derive_fernet_key_from_secret(secret_int: int) -> bytes:
    digest = hashlib.sha256(str(secret_int).encode()).digest()
    return base64.urlsafe_b64encode(digest)


def caesar_encrypt(message: str, key: int) -> str:
    return "".join(chr(ord(ch) + key) for ch in message)
