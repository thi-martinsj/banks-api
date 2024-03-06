from datetime import datetime

from sqlalchemy import (
    String,
    func
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from banks import db
from .base import (
    UUIDType,
    uuid_function
)


class Bank(db.Model):
    __tablename__ = "banks"

    id = mapped_column(UUIDType, primary_key=True, insert_default=uuid_function)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    ispb: Mapped[str] = mapped_column(String(10), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Bank(id={self.id!r}, name={self.name}, ispb={self.ispb})"
