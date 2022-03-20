from hashlib import sha384


def get_hash_for(password: str):
    return sha384(password.encode()).hexdigest()
