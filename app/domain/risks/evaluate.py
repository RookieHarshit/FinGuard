from datetime import datetime, date

from app.db.models.User.pre_user import PreUser
from app.repository.user.pre_user import PreUserRepository


class RiskDecision:
    ALLOW = "ALLOW"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


def _calculate_age(dob: date) -> int:
    today = date.today()
    return (
        today.year
        - dob.year
        - ((today.month, today.day) < (dob.month, dob.day))
    )


async def evaluate_risk(
    *,
    preuser: PreUser,
    otp_retry_count: int,
    db,
) -> str:
    """
    Evaluate onboarding risk for a PreUser.

    Hard-coded rules only.
    """

    # Rule 1: Age gate
    if preuser.date_of_birth:
        age = _calculate_age(preuser.date_of_birth)
        if age < 18:
            decision = RiskDecision.BLOCK
            reason = "UNDERAGE"
        else:
            decision = RiskDecision.ALLOW
            reason = "AGE_OK"
    else:
        decision = RiskDecision.REVIEW
        reason = "DOB_MISSING"

    # Rule 2: OTP abuse
    OTP_RETRY_THRESHOLD = 5
    if otp_retry_count > OTP_RETRY_THRESHOLD:
        decision = RiskDecision.REVIEW
        reason = "OTP_RETRY_EXCEEDED"

    repo = PreUserRepository()

    await repo.update_profile(
        db,
        preuser_id=preuser.id,
        profile_data={
            "risk_decision": decision,
            "risk_reason": reason,
            "risk_evaluated_at": datetime.utcnow(),
        },
    )

    return decision
