from abc import ABC

from banks.domain.entities import Bank


class BankRepository(ABC):
    @classmethod
    def add(cls, bank: Bank) -> Bank:
        raise NotImplementedError
