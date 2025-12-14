def _mask_phone(phone: str) -> str:
    """
    Mask a phone number for safe logging.

    Example:
        +919876543210 -> +91****10
    """
    return f"{phone[:3]}****{phone[-2:]}"
