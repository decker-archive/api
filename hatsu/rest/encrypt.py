from hashlib import sha256

def get_hash_for(password: str):
    """Resolves the lowest amount of data-leak and/or password leak possible."""
    return sha256(password.encode()).hexdigest()
