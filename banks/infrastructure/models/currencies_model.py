from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import CommonFieldsMixin


class Currency(CommonFieldsMixin):
    __tablename__ = "currencies"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    abbreviation: Mapped[str] = mapped_column(String(5), nullable=False, unique=True, index=True)
    symbol: Mapped[str] = mapped_column(String(5), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Currency( \
            id={self.id!r}, \
            name={self.name}, \
            abbreviation={self.abbreviation}, \
            symbol={self.symbol} \
        )"
