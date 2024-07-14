import datetime

from sqlalchemy import (
    Date,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import (
    CommonFieldsMixin,
    UUIDType
)
from banks.domain.enums import TransactionType


class TransactionHistory(CommonFieldsMixin):
    __tablename__ = "transactions_history"

    account_id = mapped_column(UUIDType, ForeignKey("accounts.id"), nullable=False)
    ext_account_id = mapped_column(UUIDType, ForeignKey("accounts.id"), nullable=True)
    currency_id = mapped_column(UUIDType, ForeignKey("currencies.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[TransactionType]
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False, insert_default=datetime.date.today)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
