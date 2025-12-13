import pytest
from app.core.Utils.phone import normalize_phone, InvalidPhoneNumber

def test_normalize_plain_number():
    assert normalize_phone("9876543210") == "+919876543210"

def test_normalize_with_country_code():
    assert normalize_phone("+91 98765 43210") == "+919876543210"

def test_invalid_phone():
    with pytest.raises(InvalidPhoneNumber):
        normalize_phone("12345")
