from sqlalchemy import (
    Boolean,
    ForeignKey,
    String
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy.schema import UniqueConstraint

from .base import (
    CommonFieldsMixin,
    UUIDType
)


class Account(CommonFieldsMixin):
    __tablename__ = "accounts"

    bank_id = mapped_column(UUIDType, ForeignKey("banks.id"), nullable=False)
    account_type_id = mapped_column(UUIDType, ForeignKey("account_types.id"), nullable=False)
    currency_id = mapped_column(UUIDType, ForeignKey("currencies.id"), nullable=False)
    user_id = mapped_column(UUIDType, nullable=False)
    agency: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    number: Mapped[str] = mapped_column(String(15), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, insert_default=True)

    __table_args__ = (
        UniqueConstraint("bank_id", "agency", "number", "account_type_id", name="uq_bank_agency_number_account_type"),
    )

    def __repr__(self) -> str:
        return f"Account( \
            id={self.id!r}, \
            bank_id={self.bank_id!r}, \
            account_type_id={self.account_type_id!r}, \
            currency_id={self.currency_id!r}, \
            user_id={self.user_id!r}, \
            agency={self.agency}, \
            number={self.number}, \
            is_active={self.is_active} \
        )"
