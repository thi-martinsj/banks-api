from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from banks import db


def generate_uuid_v4_for_sqlite() -> str:
    return str(uuid4())


UUIDType = UUID(as_uuid=True) if db.engine.dialect.name == 'postgresql' else db.String(36)
uuid_function = uuid4 if db.engine.dialect.name == 'postgresql' else generate_uuid_v4_for_sqlite
