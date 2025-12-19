from app.domain.auth.account_access import AccountAccess, AccountState
from app.domain.enums import AccountTier, AccountStatus


class AccountAccessDenied(Exception):
    pass


def assert_account_access(user) -> AccountAccess:
    """
    Account state enforcement

    Ensures authenticated users are authorized to access the system.
    """

    if user.status != AccountStatus.ACTIVE:
        raise AccountAccessDenied("Account is not active")

    if user.account.tier == AccountTier.LIMITED:
        return AccountAccess(
            state=AccountState.LIMITED,
            allowed_capabilities={
                "VIEW_PROFILE",
                "COMPLETE_KYC",
            },
        )

    if user.account.tier == AccountTier.FULL:
        return AccountAccess(
            state=AccountState.FULL,
            allowed_capabilities={"*"},
        )

    raise AccountAccessDenied("Invalid account state")
