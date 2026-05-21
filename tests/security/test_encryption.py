
from backend.src.security.encryption import encrypt, decrypt
def test_enc():
    assert decrypt(encrypt("abc")) == "abc"
