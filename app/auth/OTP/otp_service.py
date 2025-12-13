from app.core.redis import redis_client
from app.core.securities import generate_otp
from typing import Optional

from app.services.OTP.bruteforce import is_locked, _increment_failed_attempts, _clear_failed_attempts
from app.services.OTP.otp_exceptions import OTPException, OTPTooManyRequests, OTPRateLimitExceeded, OTPLocked, OTPExpired, OTPMismatch

OTP_EXPIRY = 300 
OTP_MAX_REQUESTS = 3

OTP_VERIFY_MAX_ATTEMPTS = 5         
OTP_VERIFY_WINDOW = 15 * 60          
OTP_LOCKOUT_TTL = 60 * 60            


async def send_otp(phone: str):
    #Check rate limit
    count_key = f"otp_count:{phone}"
    count = await redis_client.incr(count_key)

    if count == 1:
        await redis_client.expire(count_key, OTP_EXPIRY)

    if count > OTP_MAX_REQUESTS:
        raise OTPRateLimitExceeded("Too many OTP requests, Try again later")

    # Generate and store OTP
    otp = generate_otp(6)
    otp_key = f"otp:{phone}"
    await redis_client.set(otp_key, otp, ex=OTP_EXPIRY)

    # Send via provider (dummy)
    print(f"SMS to {phone}: {otp}")  # replace with real SMS API

    return True

async def verify_otp(phone: str, user_otp: str) -> bool:
    """
    Verify OTP with brute-force protection.

    Raises:
        OTPLocked: if the phone is temporarily locked due to too many failed attempts.
        OTPExpired: if there is no OTP stored / it expired.
        OTPMismatch: if the OTP is incorrect (and increments failure counter).
    Returns:
        True if verification succeeds.
    """
    if await is_locked(phone):
        raise OTPLocked("Too many failed verification attempts. Try later.")

    otp_key = f"otp:{phone}"
    saved = await redis_client.get(otp_key)

    if not saved:
        await _increment_failed_attempts(phone)
        raise OTPExpired("OTP expired or not found. Request a new OTP.")

    if saved != user_otp:
        attempts = await _increment_failed_attempts(phone)
        raise OTPMismatch(f"OTP incorrect. Attempt {attempts}/{OTP_VERIFY_MAX_ATTEMPTS}.")
    
    await redis_client.delete(otp_key)
    await _clear_failed_attempts(phone)
    return True