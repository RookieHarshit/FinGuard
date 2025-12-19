from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.domain.auth.login_decision import LoginDecision
from app.db.models.User.user_core import User
from app.domain.user.status import UserStatus


async def post_auth_router(
    *,
    db: AsyncSession,
    phone: str,
) -> LoginDecision:
    """
    STEP L1 — Identity lookup & routing

    Decides whether the flow should continue as login or onboarding
    after successful OTP verification.

    No side effects. No persistence.
    """

    result = await db.execute(
        select(User).where(User.phone == phone)
    )
    user = result.scalar_one_or_none()

    if user is None:
        return LoginDecision.ONBOARDING_REQUIRED

    if user.status != UserStatus.ACTIVE:
        return LoginDecision.DENY

    return LoginDecision.ALLOW_LOGIN
