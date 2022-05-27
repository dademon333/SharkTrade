from hashlib import sha256


def hash_password(user_id: int, password: str) -> str:
    """Returns password in hashed form, like it stores in database."""
    password = f'{password}|{user_id}'
    return sha256(password.encode()).hexdigest()
