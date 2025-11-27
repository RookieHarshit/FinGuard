from __future__ import annotations
from typing import Optional, List
from uuid import uuid4
from datetime import datetime

from decimal import Decimal 
from sqlalchemy import (
    Numeric, Enum, TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from sqlalchemy.sql import func

from app.db.models.transaction import Transaction
from app.db.models.ledger_entry import LedgerEntry
from app.db.base import Base
from app.db.enums import CurrencyCode, AccountStatus

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True))
    currency: Mapped[CurrencyCode] = mapped_column(Enum(CurrencyCode), default=CurrencyCode.INR ,nullable=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False, default=0)
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    # Reverse relationships
    sent_transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="sender_account_obj",
        foreign_keys="Transaction.sender_account",
        cascade="all, delete-orphan"
    )
    received_transactions: Mapped[List["Transaction"]] = relationship(
        back_populates="receiver_account_obj",
        foreign_keys="Transaction.receiver_account",
        cascade="all, delete-orphan"
    )
    ledger_entries: Mapped[List["LedgerEntry"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan"
    )
