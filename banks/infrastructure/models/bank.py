from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import CommonFieldsMixin


class Bank(CommonFieldsMixin):
    __tablename__ = "banks"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    ispb: Mapped[str] = mapped_column(String(10), nullable=False, unique=True, index=True)

    def __repr__(self) -> str:
        return f"Bank(id={self.id!r}, name={self.name}, ispb={self.ispb})"
