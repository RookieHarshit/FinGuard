import re

DEFAULT_COUNTRY_CODE = "91"
PHONE_DIGITS_LENGTH = 10


class InvalidPhoneNumber(Exception):
    """Raised when a phone number cannot be normalized."""
    pass


def normalize_phone(phone: str) -> str:
    """
    Normalize a phone number to a canonical E.164-like format.

    - Removes spaces and special characters
    - Ensures country code is present
    - Validates final length

    Example:
        "9876543210"      -> "+919876543210"
        "+91 98765 43210" -> "+919876543210"

    Args:
        phone (str): Raw phone number input.

    Returns:
        str: Normalized phone number in +<country><number> format.

    Raises:
        InvalidPhoneNumber: If phone number is invalid.
    """
    if not phone:
        raise InvalidPhoneNumber("Phone number is required")

    digits = re.sub(r"\D", "", phone)

    # Handle country code
    if len(digits) == PHONE_DIGITS_LENGTH:
        digits = DEFAULT_COUNTRY_CODE + digits
    elif len(digits) == PHONE_DIGITS_LENGTH + len(DEFAULT_COUNTRY_CODE):
        if not digits.startswith(DEFAULT_COUNTRY_CODE):
            raise InvalidPhoneNumber("Invalid country code")
    else:
        raise InvalidPhoneNumber("Invalid phone number length")

    return f"+{digits}"
