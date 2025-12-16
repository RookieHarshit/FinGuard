"""
PIN hashing and verification utilities for Fintech authentication.

This module is responsible for securely hashing and verifying user PINs.
It uses Argon2id with parameters tuned for resistance against offline
brute-force attacks while keeping latency acceptable for PIN-based flows.

Security notes:
- PINs are strictly numeric and validated before hashing.
- A server-side pepper is applied before hashing to add protection
  in case of database compromise.
- This module is intentionally separate from password and OTP hashing
  to allow independent security policies.

Do NOT reuse this module for passwords or OTPs.
"""

from __future__ import annotations

from passlib.context import CryptContext
from passlib.exc import UnknownHashError

from .base import get_pepper, apply_pepper

_pin_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",
    argon2__memory_cost=65536,  # 64 MB
    argon2__time_cost=3,
    argon2__parallelism=2,
    argon2__hash_len=32,
    argon2__salt_size=16,
)

def hash_pin(pin: str) -> str:
    """
    Hash a numeric PIN using Argon2id.

    The PIN is validated, peppered using a server-side secret, and then
    hashed using the configured Argon2id parameters.

    Args:
        pin: The raw numeric PIN provided by the user.

    Returns:
        A secure Argon2id hash of the peppered PIN.

    Raises:
        ValueError: If the PIN is empty or contains non-numeric characters.
        HashingError: If pepper retrieval or hashing fails.
    """
    if not pin or not pin.isdigit():
        raise ValueError("PIN must be numeric")

    pepper = get_pepper()
    peppered = apply_pepper(pin, pepper)

    return _pin_context.hash(peppered)

def verify_pin(pin: str, pin_hash: str) -> bool:
    """
    Verify a numeric PIN against a stored PIN hash.

    The PIN is validated, peppered using the current server-side pepper,
    and verified against the stored Argon2id hash.

    This function is intentionally fail-safe and returns False for any
    invalid input or verification error.

    Args:
        pin: The raw numeric PIN provided by the user.
        pin_hash: The stored Argon2id hash of the PIN.

    Returns:
        True if the PIN matches the stored hash, False otherwise.
    """
    if not pin or not pin_hash:
        return False

    if not pin.isdigit():
        return False

    try:
        pepper = get_pepper()
        peppered = apply_pepper(pin, pepper)

        return _pin_context.verify(peppered, pin_hash)
    except UnknownHashError:
        return False
    
def needs_rehash(pin_hash: str) -> bool:
    """
    Determine whether a stored PIN hash needs to be rehashed.

    This is typically used when Argon2 parameters change and existing
    hashes should be upgraded transparently after successful verification.

    Args:
        pin_hash: The stored PIN hash.

    Returns:
        True if the hash should be rehashed with current parameters,
        False otherwise.
    """
    return _pin_context.needs_update(pin_hash)
