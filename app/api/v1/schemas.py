from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal
from typing import Optional
from app.db.models import AccountStatus, TransactionStatus, CurrencyCode


class AccountCreate(BaseModel):
    currency: CurrencyCode

class AccountOut(BaseModel):
    id: UUID
    currency: CurrencyCode
    balance: Decimal
    status: AccountStatus

    class Config:
        orm_mode = True


class TransactionCreate(BaseModel):
    idempotency_key: str
    sender_account: UUID
    receiver_account: UUID
    amount: Decimal
    currency: CurrencyCode
    metadata: Optional[dict] = None


class TransactionOut(BaseModel):
    id: UUID
    status: TransactionStatus
    amount: Decimal
    currency: CurrencyCode

    class Config:
        orm_mode = True
