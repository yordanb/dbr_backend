import hashlib


def generate_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()
