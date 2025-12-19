from enum import Enum


class LoginDecision(str, Enum):
    ONBOARDING_REQUIRED = "ONBOARDING_REQUIRED"
    ALLOW_LOGIN = "ALLOW_LOGIN"
    DENY = "DENY"
