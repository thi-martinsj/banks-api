from typing import Optional
from uuid import UUID


class Bank:
    def __init__(
        self,
        name: str,
        ispb: str,
        id: Optional[UUID] = None
    ) -> None:
        self._name = name
        self._ispb = ispb
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @property
    def ispb(self) -> str:
        return self._ispb

    @property
    def id(self) -> Optional[UUID]:
        return str(self._id)

    @id.setter
    def id(self, value: UUID) -> None:
        if self._id is not None:
            raise ValueError("ID is already set.")

        self._id = value

    @property
    def dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "ispb": self.ispb
        }

    def __repr__(self) -> str:
        return f"Bank(id={self.id}, name={self.name}, ispb={self.ispb})"
