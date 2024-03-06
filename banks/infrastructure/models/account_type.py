from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import CommonFieldsMixin


class AccountType(CommonFieldsMixin):
    __tablename__ = "account_types"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)

    def __repr__(self) -> str:
        return f"AccountType(id={self.id!r}, name={self.name})"
