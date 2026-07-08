from security.security import hash_password, verify_password

def test_hash_password():
    password = "secret"
    hashed = hash_password(password)

    assert hashed != password  # Hashed should be different
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False