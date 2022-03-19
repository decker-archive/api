import ulid
from hashlib import sha256


def get_hash_for(password: str):
    return sha256(password.encode()).hexdigest()
