from datetime import datetime
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from banks import db


def generate_uuid_v4_for_sqlite() -> str:
    return str(uuid4())


UUIDType = UUID(as_uuid=True) if db.engine.dialect.name == 'postgresql' else db.String(36)
uuid_function = uuid4 if db.engine.dialect.name == 'postgresql' else generate_uuid_v4_for_sqlite


class CommonFieldsMixin(db.Model):
    __abstract__ = True

    id = mapped_column(UUIDType, primary_key=True, insert_default=uuid_function)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(insert_default=func.now(), onupdate=func.now())
