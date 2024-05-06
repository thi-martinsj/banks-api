from abc import ABC
from uuid import UUID

from banks.domain.entities import Bank


class BankRepository(ABC):
    @classmethod
    def add(cls, bank: Bank) -> Bank:
        raise NotImplementedError

    @classmethod
    def list(cls, offset: int = 0, limit: int = 50, **kwargs) -> list[Bank]:
        raise NotImplementedError

    @classmethod
    def get(cls, bank_id: UUID) -> Bank:
        raise NotImplementedError

    @classmethod
    def update(cls, bank: Bank) -> Bank:
        raise NotImplementedError

    @classmethod
    def delete(cls, bank_id: UUID) -> None:
        raise NotImplementedError
