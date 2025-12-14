import pytest
from unittest.mock import AsyncMock

from app.auth.OTP.service import verify_otp
from app.auth.OTP.otp_exceptions import (
    OTPLocked,
    OTPExpired,
    OTPMismatch,
)
from app.core.security.otp import OTP_VERIFY_MAX_ATTEMPTS


@pytest.mark.asyncio
async def test_verify_otp_locked_phone_raises(mocker):
    phone = "+919876543210"

    mocker.patch(
        "app.auth.OTP.service.normalize_phone",
        return_value=phone
    )

    mocker.patch(
        "app.auth.OTP.service.is_locked",
        new=AsyncMock(return_value=True)
    )

    redis_get = mocker.patch(
        "app.auth.OTP.service.redis_client.get",
        new=AsyncMock()
    )

    with pytest.raises(OTPLocked):
        await verify_otp(phone, "123456")

    redis_get.assert_not_called()
