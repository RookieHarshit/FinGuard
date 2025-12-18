from __future__ import annotations

from dataclasses import dataclass

from app.db.models.User.pre_user import PreUser


@dataclass(slots=True)
class RiskResult:
    """
    Represents the outcome of a risk evaluation.

    Attributes:
        passed (bool): Indicates whether the subject passed all risk checks.
        reason (str | None): Optional machine-readable reason for failure.
            Should be populated only when passed is False.
    """

    passed: bool
    reason: str | None = None


async def run_risk_checks(preuser: PreUser) -> RiskResult:
    """
    Execute hard-stop risk checks for a PreUser.

    This function encapsulates domain-level risk evaluation logic
    that determines whether a PreUser is allowed to proceed further
    in the onboarding or transaction flow.

    The function is intentionally async to allow future integration
    with external systems such as:
        - Velocity / rate-limit services
        - Device fingerprinting providers
        - Blacklists / fraud databases
        - Internal risk engines

    Args:
        preuser (PreUser): The PreUser entity to be evaluated.

    Returns:
        RiskResult: The result of the risk evaluation, indicating
        whether the user passed the checks and, if not, the reason.

    Notes:
        This implementation contains placeholder logic suitable
        for portfolio or scaffolding purposes and should be extended
        for real-world usage.
    """

    # Portfolio-safe placeholder logic
    if preuser.phone.startswith("000"):
        return RiskResult(passed=False, reason="blocked_phone")

    return RiskResult(passed=True)
