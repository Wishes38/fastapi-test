import pytest
from passlib.exc import UnknownHashError
from app.core.security import get_password_hash, verify_password

# Test 1: Şifre doğru hashleniyor ve doğrulanıyor mu? (Pozitif)
def test_password_hashing_cycle():
    password = "secret_password"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed) is True

# Test 2: Yanlış şifre reddediliyor mu? (Negatif)
def test_password_verification_fail():
    password = "secret"
    hashed = get_password_hash(password)
    assert verify_password("wrong_secret", hashed) is False

# Test 3: Boş şifre hashleme (Edge Case)
def test_empty_password():
    password = ""
    hashed = get_password_hash(password)
    assert verify_password("", hashed) is True

# Test 4: Rastgele string hash kontrolü
def test_random_string_verification():

    with pytest.raises(UnknownHashError):
        verify_password("sifre123", "rastgele_bozuk_hash")