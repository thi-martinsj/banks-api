from abc import ABC

from banks.domain.entities import Bank


class BankRepository(ABC):
    @classmethod
    def add(cls, bank: Bank) -> Bank:
        raise NotImplementedError

    @classmethod
    def list(cls, offset: int = 0, limit: int = 50, **kwargs) -> list[Bank]:
        raise NotImplementedError

    @classmethod
    def get(cls, bank_id: str) -> Bank:
        raise NotImplementedError

    @classmethod
    def update(cls, bank: Bank) -> Bank:
        raise NotImplementedError
