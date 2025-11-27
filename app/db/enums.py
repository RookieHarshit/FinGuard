from enum import Enum as PyEnum

class AccountStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class TransactionStatus(str, PyEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    FLAGGED = "FLAGGED"

class CurrencyCode(str, PyEnum):
    USD = "USD"
    INR = "INR"
    EUR = "EUR"

class LedgerEntryType(str, PyEnum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

