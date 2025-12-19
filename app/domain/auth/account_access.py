from enum import Enum
from typing import Set


class AccountState(str, Enum):
    BLOCKED = "BLOCKED"
    LIMITED = "LIMITED"
    FULL = "FULL"


class AccountAccess:
    def __init__(
        self,
        *,
        state: AccountState,
        allowed_capabilities: Set[str] | None = None,
    ):
        self.state = state
        self.allowed_capabilities = allowed_capabilities or set()
